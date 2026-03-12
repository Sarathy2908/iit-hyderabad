<template>
  <div class="max-w-5xl mx-auto pb-20">
    <header class="flex items-center justify-between mb-8">
      <div>
        <h1 class="text-3xl font-black text-white px-1">Credit Appraisal Memo</h1>
        <p class="text-slate-500 mt-1 px-1">Internal Document • Confidential</p>
      </div>
      <button class="flex items-center gap-2 px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-2xl transition-all shadow-xl shadow-blue-500/20 active:scale-95">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a2 2 0 002 2h12a2 2 0 002-2v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
        Download PDF
      </button>
    </header>

    <div class="bg-white text-slate-900 rounded-[2rem] shadow-2xl p-12 min-h-[1000px] border border-slate-200">
      <!-- Watermark -->
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 rotate-45 text-slate-100 text-8xl font-black pointer-events-none select-none opacity-50">
        INTELLI-CREDIT
      </div>

      <div class="relative z-10 space-y-12">
        <div class="flex justify-between border-b-2 border-slate-900 pb-8">
          <div class="space-y-1">
            <h2 class="text-2xl font-black uppercase">CAM #2026-TS-001</h2>
            <p class="text-sm font-bold text-slate-500">Date: March 12, 2026</p>
          </div>
          <div class="text-right">
            <p class="text-sm font-bold">Lending Division</p>
            <p class="text-sm">Corporate Credit Dept.</p>
          </div>
        </div>

        <section>
          <h3 class="text-lg font-black uppercase text-blue-600 mb-4 tracking-wider">I. Executive Summary</h3>
          <p class="text-sm leading-relaxed text-slate-700">
            Tata Steel Ltd (the "Borrower") seeks a working capital facility of ₹ 450 Cr. Based on the AI-powered assessment, the borrower demonstrates strong liquidity (Current Ratio 1.45x) and exceptional profitability (EBITDA margin 18%). News sentiment is predominantly positive, driven by strong quarterly performance and domestic infrastructure demand.
          </p>
        </section>

        <section>
          <h3 class="text-lg font-black uppercase text-blue-600 mb-4 tracking-wider">II. Financial Snapshot</h3>
          <div class="grid grid-cols-3 gap-8 py-6 px-8 bg-slate-50 rounded-2xl border border-slate-100">
            <div v-for="s in [{l:'Revenue YoY', v:'+18.2%'}, {l:'Net Worth', v:'₹ 8,450 Cr'}, {l:'D/E Ratio', v:'0.42'}]" :key="s.l">
              <p class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">{{ s.l }}</p>
              <p class="text-xl font-bold text-slate-900">{{ s.v }}</p>
            </div>
          </div>
        </section>

        <section>
          <h3 class="text-lg font-black uppercase text-blue-600 mb-4 tracking-wider">III. Risk Intelligence & Sentiment</h3>
          <div class="space-y-4">
             <div class="p-4 border-l-4 border-emerald-500 bg-emerald-50 px-6">
                <p class="text-[10px] font-black text-emerald-700 uppercase mb-1">Market Sentiment</p>
                <p class="text-sm italic">"High domestic demand and expansion into european markets driving 68% positive sentiment scoring."</p>
             </div>
             <div class="p-4 border-l-4 border-amber-500 bg-amber-50 px-6">
                <p class="text-[10px] font-black text-amber-700 uppercase mb-1">Regulatory Watch</p>
                <p class="text-sm italic">"Active litigation found in 2 cases regarding vendor payments; aggregate exposure below ₹ 5 Cr (Low Materiality)."</p>
             </div>
          </div>
        </section>

        <section>
          <h3 class="text-lg font-black uppercase text-blue-600 mb-4 tracking-wider">IV. Lending Recommendation</h3>
          <div class="border-2 border-slate-900 p-8 rounded-3xl">
             <div class="flex items-center justify-between mb-6">
                <span class="text-4xl font-black text-slate-900">APPROVE</span>
                <div class="text-right">
                   <p class="text-xs font-bold text-slate-400 uppercase">Limit Recommended</p>
                   <p class="text-2xl font-black text-slate-900">₹ 450,00,00,000</p>
                </div>
             </div>
             <div class="grid grid-cols-2 gap-8 text-sm pt-6 border-t border-slate-200">
                <p><span class="font-bold">Interest Rate:</span> repo + 180 bps</p>
                <p><span class="font-bold">Tenor:</span> 36 Months</p>
                <p><span class="font-bold">Security:</span> Exclusive charge on fixed assets</p>
                <p><span class="font-bold">Repayment:</span> Monthly installments</p>
             </div>
          </div>
        </section>

        <div class="pt-20 flex justify-between">
           <div class="border-t border-slate-400 pt-2 w-48 text-center text-xs font-bold text-slate-500">Intelli-Credit AI Sign-off</div>
           <div class="border-t border-slate-400 pt-2 w-48 text-center text-xs font-bold text-slate-500">Credit Manager Signature</div>
        </div>
      </div>
    </div>
  </div>
</template>
