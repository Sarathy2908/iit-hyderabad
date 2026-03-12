import { onObjectFinalized } from "firebase-functions/v2/storage";
import { onCall, CallableRequest } from "firebase-functions/v2/https";
import { onDocumentUpdated } from "firebase-functions/v2/firestore";
import * as admin from 'firebase-admin';
import axios from 'axios';
import { handleDocumentUpload } from './ingestor/orchestrator';
import { generateCAM } from './cam/generator';

admin.initializeApp();

const ML_SERVICE_URL = process.env.ML_SERVICE_URL || 'http://localhost:8080';

// Storage trigger (Gen 2)
export const onDocumentUpload = onObjectFinalized(async (event) => {
  return handleDocumentUpload(event.data);
});

// Helper to call ML Service
async function callMLService(endpoint: string, data: any) {
  try {
    const response = await axios.post(`${ML_SERVICE_URL}/${endpoint}`, data);
    return response.data;
  } catch (error) {
    console.error(`ML Service Error (${endpoint}):`, error);
    throw error;
  }
}

// Research Agent trigger (Blueprint: case status = INGESTING complete)
export const onIngestionComplete = onDocumentUpdated("cases/{caseId}", async (event) => {
  const before = event.data?.before.data();
  const after = event.data?.after.data();
  
  if (before?.status !== 'RESEARCHING' && after?.status === 'RESEARCHING') {
      console.log(`Starting research agent for case: ${event.params.caseId}`);
      // Launch Puppeteer crawler logic would go here
      // For MVP, we simulate research completion
      await admin.firestore().doc(`cases/${event.params.caseId}`).update({
          researchFindings: { sentiment: 'positive', newsCount: 5 },
          status: 'SCORING_READY',
          updatedAt: admin.firestore.FieldValue.serverTimestamp()
      });
  }
});

// CAM Generation trigger (Blueprint: scoreResult written)
export const onScoreResultWritten = onDocumentUpdated("cases/{caseId}", async (event) => {
  const after = event.data?.after.data();
  const before = event.data?.before.data();

  if (!before?.scoreResult && after?.scoreResult) {
      console.log(`Score result detected. Generating CAM for: ${event.params.caseId}`);
      await generateCAM(event.params.caseId);
  }
});

// HTTP Callable for manual scoring (Gen 2)
export const runScoringEngine = onCall(async (request: CallableRequest) => {
  const { caseId, features } = request.data;
  console.log(`Triggering scoring for case: ${caseId}`);
  
  const scoreResult = await callMLService('score', { features });
  
  await admin.firestore().doc(`cases/${caseId}`).update({
    scoreResult,
    status: 'COMPLETE',
    updatedAt: admin.firestore.FieldValue.serverTimestamp()
  });

  return { status: 'success', result: scoreResult };
});
