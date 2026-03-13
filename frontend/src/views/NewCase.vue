<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { 
  ChevronLeft, 
  Sparkles, 
  CheckCircle2, 
  UserCircle, 
  FileUp, 
  Loader2, 
  Send, 
  Info, 
  ShieldCheck 
} from 'lucide-vue-next'
import { collection, addDoc, serverTimestamp, updateDoc } from 'firebase/firestore'
import { ref as sRef, uploadBytes, getDownloadURL } from 'firebase/storage'
import { db, storage } from '../firebase'
import UploadZone from '../components/UploadZone.vue'

const router = useRouter()
const borrowerName = ref('')
const borrowerCIN = ref('')
const requestedLimit = ref<number | string>('')
const uploadedFiles = ref<File[]>([])
const isSubmitting = ref(false)
const isSuccess = ref(false)

const isFormValid = computed(() => {
  return borrowerName.value.length > 2 && borrowerCIN.value.length > 5
})

async function handleSubmit() {
  if (!isFormValid.value) return
  
  isSubmitting.value = true
  try {
    // 1. Create the case document first to get the ID
    const docRef = await addDoc(collection(db, 'cases'), {
      name: borrowerName.value,
      cin: borrowerCIN.value,
      limit: requestedLimit.value || 0,
      status: 'In Queue',
      date: new Date().toISOString().split('T')[0],
      score: 0,
      dscr: '-',
      de: '-',
      timestamp: serverTimestamp(),
      newsItems: [],
      ratios: [],
      sentiment: { positive: 0, negative: 0, neutral: 100 },
      documents: []
    })

    const caseId = docRef.id
    // 2. Upload files to Storage in parallel
    const uploadPromises = uploadedFiles.value.map(async (file) => {
      const storagePath = `cases/${caseId}/documents/${file.name}`
      const storageReference = sRef(storage, storagePath)
      const uploadResult = await uploadBytes(storageReference, file)
      const downloadUrl = await getDownloadURL(uploadResult.ref)
      
      return {
        name: file.name,
        url: downloadUrl,
        type: file.type,
        size: file.size,
        uploadedAt: new Date().toISOString()
      }
    })

    const documentUrls = await Promise.all(uploadPromises)

    // 3. Update the Firestore document with the actual document URLs
    if (documentUrls.length > 0) {
      await updateDoc(docRef, {
        documents: documentUrls,
        status: 'Processing' // Change status once docs are uploaded
      })
    }
    
    isSuccess.value = true
    router.push(`/case/${caseId}`)
  } catch (error) {
    console.error("Error during submission: ", error)
    alert("Failed to initiate appraisal. Error: " + (error instanceof Error ? error.message : "Unknown error"))
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="max-w-7xl mx-auto pb-24 px-4 sm:px-6 lg:px-8">
    <header class="mb-16">
       <button @click="$router.back()" class="flex items-center gap-2.5 text-[var(--text-muted)] hover:text-[var(--text-heading)] transition-all mb-10 group active:scale-95">
         <div class="p-2 rounded-xl bg-[var(--surface-1)] border border-[var(--border-main)] group-hover:bg-[var(--surface-2)] transition-colors">
           <ChevronLeft class="w-5 h-5 transform group-hover:-translate-x-1 transition-transform" />
         </div>
         <span class="font-black text-xs uppercase tracking-[0.2em] opacity-80 group-hover:opacity-100">Back to Dashboard</span>
       </button>
       <div class="flex items-center gap-6">
         <div class="w-16 h-16 rounded-[2rem] bg-primary/10 text-primary flex items-center justify-center border-2 border-primary/20 shadow-xl shadow-primary/5">
           <Sparkles class="w-8 h-8" />
         </div>
         <div>
           <h1 class="text-5xl font-black text-[var(--text-heading)] tracking-tighter">Initiate Appraisal</h1>
           <p class="text-[var(--text-main)] mt-2 font-black italic opacity-60 flex items-center gap-3">
             <div class="w-2 h-2 rounded-full bg-primary/30"></div>
             Upload corporate documentation to begin the AI-powered credit assessment.
           </p>
         </div>
       </div>
    </header>

    <div v-if="isSuccess" class="flex flex-col items-center justify-center py-32 bg-[var(--surface-raised)] rounded-[4rem] border border-[var(--border-main)] shadow-2xl animate-in fade-in zoom-in duration-700 relative overflow-hidden">
       <div class="absolute inset-0 bg-primary/5 blur-[120px] pointer-events-none"></div>
       <div class="w-32 h-32 rounded-[3rem] bg-[var(--color-success-muted)] text-[var(--color-success)] flex items-center justify-center mb-10 border-2 border-[var(--color-success)]/20 shadow-2xl shadow-[var(--color-success)]/20 relative z-10 animate-bounce">
         <CheckCircle2 class="w-16 h-16" />
       </div>
       <h2 class="text-4xl font-black text-[var(--text-heading)] mb-4 tracking-tighter relative z-10">Submission Successful</h2>
       <p class="text-[var(--text-main)] text-xl font-black opacity-40 relative z-10">Redirecting to monitoring engine...</p>
    </div>

    <div v-else class="grid grid-cols-1 lg:grid-cols-12 gap-16">
      <div class="lg:col-span-8 space-y-12">
        <section class="bg-[var(--surface-raised)] border border-[var(--border-main)] rounded-[3rem] p-12 shadow-sm relative overflow-hidden group">
          <div class="absolute -top-10 -right-10 w-40 h-40 bg-primary/5 blur-3xl group-hover:bg-primary/10 transition-colors"></div>
          <h2 class="text-2xl font-black text-[var(--text-heading)] mb-12 flex items-center gap-5 relative z-10">
            <div class="w-12 h-12 rounded-2xl bg-primary/10 text-primary flex items-center justify-center border border-primary/20 shadow-lg shadow-primary/5 group-hover:scale-110 transition-transform duration-500">
              <UserCircle class="w-7 h-7" />
            </div>
            Borrower Profile
          </h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-10 pl-4 relative z-10">
            <div class="space-y-4">
              <label class="text-[10px] font-black text-[var(--text-label)] uppercase tracking-[0.3em] pl-1 opacity-60">Legal Entity Name</label>
              <div class="relative group/input">
                <input 
                  v-model="borrowerName"
                  type="text" 
                  placeholder="e.g. Acme Corp Ltd" 
                  class="w-full bg-[var(--surface-1)] border-2 border-[var(--border-main)] rounded-[1.8rem] px-8 py-5 text-[var(--text-heading)] font-black focus:border-primary/50 focus:bg-[var(--surface-raised)] focus:ring-[12px] focus:ring-primary/5 transition-all outline-none placeholder:text-[var(--text-muted)] placeholder:font-black placeholder:opacity-30 text-lg shadow-inner"
                >
                <div class="absolute inset-0 rounded-[1.8rem] border border-primary/0 group-hover/input:border-primary/20 pointer-events-none transition-colors"></div>
              </div>
            </div>
            <div class="space-y-4">
              <label class="text-[10px] font-black text-[var(--text-label)] uppercase tracking-[0.3em] pl-1 opacity-60">Registration (CIN)</label>
              <div class="relative group/input">
                <input 
                  v-model="borrowerCIN"
                  type="text" 
                  placeholder="U12345MH2023PTC123456" 
                  class="w-full bg-[var(--surface-1)] border-2 border-[var(--border-main)] rounded-[1.8rem] px-8 py-5 text-[var(--text-heading)] font-black focus:border-primary/50 focus:bg-[var(--surface-raised)] focus:ring-[12px] focus:ring-primary/5 transition-all outline-none placeholder:text-[var(--text-muted)] placeholder:font-black placeholder:opacity-30 text-lg shadow-inner"
                >
                <div class="absolute inset-0 rounded-[1.8rem] border border-primary/0 group-hover/input:border-primary/20 pointer-events-none transition-colors"></div>
              </div>
            </div>
            <div class="space-y-4">
              <label class="text-[10px] font-black text-[var(--text-label)] uppercase tracking-[0.3em] pl-1 opacity-60">Requested Limit (Cr)</label>
              <div class="relative group/input">
                <input 
                  v-model="requestedLimit"
                  type="number" 
                  placeholder="e.g. 150" 
                  class="w-full bg-[var(--surface-1)] border-2 border-[var(--border-main)] rounded-[1.8rem] px-8 py-5 text-[var(--text-heading)] font-black focus:border-primary/50 focus:bg-[var(--surface-raised)] focus:ring-[12px] focus:ring-primary/5 transition-all outline-none placeholder:text-[var(--text-muted)] placeholder:font-black placeholder:opacity-30 text-lg shadow-inner"
                >
                <div class="absolute inset-0 rounded-[1.8rem] border border-primary/0 group-hover/input:border-primary/20 pointer-events-none transition-colors"></div>
              </div>
            </div>
          </div>
        </section>

        <section class="bg-[var(--surface-raised)] border border-[var(--border-main)] rounded-[3rem] p-12 shadow-sm relative overflow-hidden group">
          <h2 class="text-2xl font-black text-[var(--text-heading)] mb-12 flex items-center gap-5 relative z-10">
            <div class="w-12 h-12 rounded-2xl bg-primary/10 text-primary flex items-center justify-center border border-primary/20 shadow-lg shadow-primary/5 group-hover:scale-110 transition-transform duration-500">
              <FileUp class="w-7 h-7" />
            </div>
            Document Ingestion
          </h2>
          <div class="pl-4">
            <UploadZone @update:files="uploadedFiles = $event" />
          </div>
        </section>

        <div class="flex justify-end pt-4">
          <button 
            @click="handleSubmit"
            :disabled="!isFormValid || isSubmitting"
            class="flex items-center gap-5 px-16 py-7 bg-primary hover:bg-primary-hover text-white font-black rounded-[2.5rem] transition-all shadow-2xl shadow-primary/20 active:scale-95 group disabled:opacity-30 disabled:cursor-not-allowed disabled:grayscale uppercase tracking-[0.3em] text-xs relative overflow-hidden"
          >
            <div class="absolute inset-0 bg-gradient-to-r from-white/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
            <Loader2 v-if="isSubmitting" class="w-5 h-5 animate-spin" />
            <template v-else>
              Submit for Appraisal
              <Send class="w-6 h-6 transform group-hover:translate-x-1 group-hover:-translate-y-1 transition-transform" />
            </template>
          </button>
        </div>
      </div>

      <aside class="lg:col-span-4 space-y-12">
        <div class="bg-primary/5 border border-primary/10 rounded-[3rem] p-10 relative overflow-hidden group">
          <div class="absolute -bottom-10 -left-10 w-32 h-32 bg-primary/10 blur-3xl"></div>
          <div class="flex items-center gap-4 mb-10">
            <div class="w-12 h-12 rounded-2xl bg-primary/10 text-primary flex items-center justify-center border border-primary/20 shadow-sm">
              <Info class="w-6 h-6" />
            </div>
            <h3 class="text-xl font-black text-primary tracking-tight">Ingestion Guide</h3>
          </div>
          <ul class="space-y-10 pl-2">
            <li v-for="guide in [
              {t:'Clean Documents', d:'Ensure PDFs are not password protected.', i: ShieldCheck},
              {t:'GST Returns', d:'Upload GSTR-1, 2A, and 3B for 12 months.', i: CheckCircle2},
              {t:'Bank Statements', d:'Prefer CSV for 5x faster processing.', i: Sparkles}
            ]" :key="guide.t" class="flex gap-6 group/item">
              <div class="w-1.5 h-1.5 rounded-full bg-primary/40 mt-2.5 group-hover/item:scale-150 group-hover/item:bg-primary transition-all"></div>
              <div>
                <p class="text-[11px] font-black text-[var(--text-heading)] uppercase tracking-[0.2em] group-hover/item:text-primary transition-colors">{{ guide.t }}</p>
                <p class="text-[13px] text-[var(--text-main)] leading-relaxed mt-2 font-black opacity-60">"{{ guide.d }}"</p>
              </div>
            </li>
          </ul>
        </div>
        
        <div class="bg-[var(--surface-raised)] border border-[var(--border-main)] rounded-[3rem] p-10 shadow-sm group">
           <div class="flex items-center gap-4 mb-8">
             <div class="w-10 h-10 rounded-xl bg-[var(--color-success-muted)] text-[var(--color-success)] flex items-center justify-center border border-[var(--color-success)]/20">
               <ShieldCheck class="w-6 h-6" />
             </div>
             <p class="text-[10px] font-black text-[var(--text-label)] uppercase tracking-[0.3em] opacity-60">Security Protocol</p>
           </div>
           <div class="pl-4 border-l-2 border-[var(--border-main)] group-hover:border-[var(--color-success)]/30 transition-colors">
             <p class="text-sm text-[var(--text-main)] leading-relaxed font-black opacity-40 italic">
               "All documents are encrypted at rest and processed in-house. Zero data leakage policy."
             </p>
           </div>
        </div>
      </aside>
    </div>
  </div>
</template>
