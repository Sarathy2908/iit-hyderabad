import * as admin from 'firebase-admin';
import * as PizZip from 'pizzip';
import Docxtemplater from 'docxtemplater';

export async function generateCAM(caseId: string) {
  console.log(`Generating CAM for case ${caseId}`);
  
  const db = admin.firestore();
  const caseDoc = await db.doc(`cases/${caseId}`).get();
  const caseData = caseDoc.data();

  if (!caseData) {
    console.error('Case data not found');
    return;
  }

  // In a real scenario, we would load a .docx template from Storage
  // For MVP/Demo, we describe the logic
  
  const data = {
    companyName: caseData.companyName,
    caseId: caseId,
    date: new Date().toLocaleDateString(),
    score: caseData.scoreResult?.score || 0,
    recommendation: caseData.scoreResult?.recommendation || 'PENDING',
    dscr: caseData.financials?.dscr || 'N/A',
    deRatio: caseData.financials?.deRatio || 'N/A',
    rationale: caseData.scoreResult?.rationale || 'Assessment in progress.'
  };

  console.log('Template data:', data);

  // Simulation of Word generation
  // const zip = new PizZip(content);
  // const doc = new Docxtemplater(zip, { paragraphLoop: true, linebreaks: true });
  // doc.render(data);
  // const buf = doc.getZip().generate({ type: 'nodebuffer' });
  
  const mockCamUrl = `https://storage.googleapis.com/intelli-credit/cams/${caseId}_CAM.docx`;
  
  await db.doc(`cases/${caseId}`).update({
    camUrl: mockCamUrl,
    status: 'COMPLETE',
    updatedAt: admin.firestore.FieldValue.serverTimestamp()
  });

  console.log(`CAM generation complete for ${caseId}`);
}
