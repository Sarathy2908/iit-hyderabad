import * as admin from 'firebase-admin';
import { analyzeGST } from './gst-analyser';
import { parseBankStatement } from './bank-parser';

export async function handleDocumentUpload(object: any) {
  const filePath = object.name; // e.g. cases/caseId/documents/filename.pdf
  const fileName = filePath.split('/').pop();
  const caseId = filePath.split('/')[1];

  if (!caseId || !fileName) {
    console.error('Invalid file path structure');
    return null;
  }

  const db = admin.firestore();
  await db.doc(`cases/${caseId}`).update({
    status: 'INGESTING',
    updatedAt: admin.firestore.FieldValue.serverTimestamp()
  });

  const fileExt = fileName.split('.').pop()?.toLowerCase();

  try {
    if (fileExt === 'json' || fileExt === 'xml') {
      // Likely GST or structured financial data
      console.log(`Processing GST/XML data: ${fileName}`);
      await analyzeGST(caseId, filePath);
    } else if (fileExt === 'csv') {
      // Likely bank statement
      console.log(`Processing CSV bank statement: ${fileName}`);
      await parseBankStatement(caseId, filePath);
    } else if (fileExt === 'pdf') {
      // Unstructured document - would call ML NER service in real scenario
      console.log(`Processing PDF: ${fileName}`);
      await db.doc(`cases/${caseId}`).update({
        'ingestionFlags.pdfReceived': true
      });
    }

    // After each successful ingestion, check if we should move to RESEARCHING
    // For MVP, we just move to RESEARCHING after first document
    await db.doc(`cases/${caseId}`).update({
      status: 'RESEARCHING'
    });

  } catch (error) {
    console.error(`Error processing ${fileName}:`, error);
    await db.doc(`cases/${caseId}`).update({
      status: 'ERROR'
    });
  }

  return null;
}
