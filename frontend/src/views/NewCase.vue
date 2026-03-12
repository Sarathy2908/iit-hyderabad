<script setup lang="ts">
import UploadZone from '../components/UploadZone.vue'
</script>

<template>
  <div class="max-w-4xl mx-auto pb-20">
    <header class="mb-12">
       <button @click="$router.back()" class="flex items-center gap-2 text-slate-500 hover:text-white transition-colors mb-6 group">
         <svg class="w-4 h-4 transform group-hover:-translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/></svg>
         Back to Dashboard
       </button>
       <h1 class="text-4xl font-black text-white tracking-tight">Initiate Appraisal</h1>
       <p class="text-slate-400 mt-2">Upload corporate documentation to begin the AI-powered credit assessment.</p>
    </header>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-12">
      <div class="lg:col-span-2 space-y-8">
        <section class="bg-slate-900 border border-slate-800 rounded-3xl p-8">
          <h2 class="text-xl font-bold text-white mb-6 flex items-center gap-3">
            <span class="w-8 h-8 rounded-full bg-blue-500/20 text-blue-400 flex items-center justify-center text-sm">1</span>
            Borrower Profile
          </h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="space-y-2">
              <label class="text-xs font-bold text-slate-500 uppercase tracking-widest pl-1">Legal Entity Name</label>
              <input type="text" placeholder="e.g. Acme Corp Ltd" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-slate-200 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all outline-none">
            </div>
            <div class="space-y-2">
              <label class="text-xs font-bold text-slate-500 uppercase tracking-widest pl-1">Registration Number (CIN)</label>
              <input type="text" placeholder="U12345MH2023PTC123456" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-slate-200 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all outline-none">
            </div>
          </div>
        </section>

        <section class="bg-slate-900 border border-slate-800 rounded-3xl p-8">
          <h2 class="text-xl font-bold text-white mb-6 flex items-center gap-3">
            <span class="w-8 h-8 rounded-full bg-blue-500/20 text-blue-400 flex items-center justify-center text-sm">2</span>
            Document Ingestion
          </h2>
          <UploadZone />
        </section>

        <div class="flex justify-end">
          <button class="px-10 py-4 bg-blue-600 hover:bg-blue-700 text-white font-black rounded-2xl transition-all shadow-xl shadow-blue-500/10 active:scale-95">
            SUBMIT FOR ANALYSIS
          </button>
        </div>
      </div>

      <aside class="space-y-6">
        <div class="bg-blue-600/5 border border-blue-500/10 rounded-3xl p-6">
          <h3 class="text-lg font-bold text-blue-400 mb-4">Ingestion Guide</h3>
          <ul class="space-y-4">
            <li v-for="guide in [
              {t:'Clean Documents', d:'Ensure PDFs are not password protected.'},
              {t:'GST Returns', d:'Upload GSTR-1, 2A, and 3B for the last 12 months.'},
              {t:'Bank Statements', d:'Prefer CSV format for faster processing.'}
            ]" :key="guide.t">
              <p class="text-sm font-bold text-slate-200">{{ guide.t }}</p>
              <p class="text-xs text-slate-500 leading-relaxed">{{ guide.d }}</p>
            </li>
          </ul>
        </div>
        
        <div class="bg-slate-900 border border-slate-800 rounded-3xl p-6">
           <p class="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-4">Security</p>
           <p class="text-xs text-slate-400 leading-relaxed italic">
             "All uploaded documents are encrypted at rest and processed by in-house ML models. No data leaves our secure network."
           </p>
        </div>
      </aside>
    </div>
  </div>
</template>
