<template>
  <div class="max-w-6xl mx-auto pb-20 space-y-12">
    <header>
      <h1 class="text-4xl font-black text-white tracking-tight">System Configuration</h1>
      <p class="text-slate-400 mt-2">Manage scoring weights, sector benchmarks, and risk thresholds.</p>
    </header>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
      <!-- Scoring Weights -->
      <section class="bg-slate-900 border border-slate-800 rounded-3xl p-8">
        <h2 class="text-xl font-bold text-white mb-8 flex items-center justify-between">
          Scoring Engine Calibration
          <span class="text-xs font-medium text-slate-500 italic">Total: 100%</span>
        </h2>
        <div class="space-y-8">
          <div v-for="w in [
            {l:'Financial Ratios (Capacity)', v:40},
            {l:'News Sentiment (Character)', v:25},
            {l:'Historical Repayment', v:20},
            {l:'Qualitative Overrides', v:15}
          ]" :key="w.l" class="space-y-4">
             <div class="flex justify-between items-center">
                <span class="text-sm font-bold text-slate-300">{{ w.l }}</span>
                <span class="text-sm font-bold text-blue-400">{{ w.v }}%</span>
             </div>
             <div class="h-2 w-full bg-slate-800 rounded-full overflow-hidden">
                <div class="h-full bg-blue-500" :style="{ width: w.v + '%' }"></div>
             </div>
          </div>
        </div>
        <button class="w-full mt-10 py-4 bg-blue-600 hover:bg-blue-700 text-white font-black rounded-2xl transition-colors">
          Update Model Weights
        </button>
      </section>

      <!-- Sector Benchmarks -->
      <section class="bg-slate-900 border border-slate-800 rounded-3xl p-8">
        <h2 class="text-xl font-bold text-white mb-8">Sector Risk Benchmarks</h2>
        <div class="space-y-4">
           <table class="w-full text-left">
             <thead class="text-[10px] font-black text-slate-500 uppercase tracking-widest border-b border-slate-800">
               <tr>
                 <th class="py-4">Sector</th>
                 <th class="py-4">Avg. DSCR</th>
                 <th class="py-4">Risk Level</th>
                 <th class="py-4">Status</th>
               </tr>
             </thead>
             <tbody class="text-sm text-slate-300">
               <tr v-for="row in [
                 {s:'Steel', a:'1.25x', r:'Low', c:'text-emerald-400'},
                 {s:'Infrastructure', a:'1.1x', r:'Moderate', c:'text-amber-400'},
                 {s:'Real Estate', a:'0.85x', r:'High', c:'text-red-400'},
                 {s:'IT / SaaS', a:'2.4x', r:'Minimal', c:'text-blue-400'}
               ]" :key="row.s" class="border-b border-slate-800/50">
                 <td class="py-4 font-bold">{{ row.s }}</td>
                 <td class="py-4">{{ row.a }}</td>
                 <td class="py-4" :class="row.c">{{ row.r }}</td>
                 <td class="py-4">
                    <button class="p-1 hover:text-blue-400 transition-colors">
                       <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z"/></svg>
                    </button>
                 </td>
               </tr>
             </tbody>
           </table>
        </div>
      </section>
    </div>

    <!-- Alert Thresholds -->
    <div class="bg-slate-900 border border-slate-800 rounded-3xl p-8">
       <h2 class="text-xl font-bold text-white mb-6">Real-time Warning Thresholds</h2>
       <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div v-for="t in [
            {t:'GST Variance', v:'> 15%', d:'Flag gap between 2A and 3B.'},
            {t:'News Multiplier', v:'3x', d:'Weight for negative regulatory news.'},
            {t:'Cheque Bounce', v:'2/qr', d:'Max frequency before automatic score downgrade.'}
          ]" :key="t.t" class="p-6 bg-slate-950 rounded-2xl border border-slate-800">
             <div class="flex items-center justify-between mb-2">
                <span class="text-xs font-bold text-slate-200">{{ t.t }}</span>
                <span class="text-xs font-black text-blue-400">{{ t.v }}</span>
             </div>
             <p class="text-[11px] text-slate-500 leading-relaxed">{{ t.d }}</p>
          </div>
       </div>
    </div>
  </div>
</template>
