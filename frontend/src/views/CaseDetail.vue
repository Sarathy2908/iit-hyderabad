<script setup lang="ts">
import { ref } from 'vue'
import ScoreGauge from '../components/ScoreGauge.vue'
import FinancialRatioCard from '../components/FinancialRatioCard.vue'
import ResearchFeed from '../components/ResearchFeed.vue'

const activeTab = ref('financials')

const newsItems = [
  { id: '1', title: 'Tata Steel Q3 Profit Surges 15% on Strong Domestic Demand', source: 'Economic Times', date: '2 days ago', sentiment: 'positive', summary: 'Net profit rose to ₹2,450 crore, beating street estimates. Infrastructure push in India driving steel consumption.' },
  { id: '2', title: 'Director Resignation: Board Member Cites Personal Reasons', source: 'Business Standard', date: '1 week ago', sentiment: 'neutral' },
  { id: '3', title: 'GSTR-2A Matching Discrepancy Found in Recent Audit', source: 'Internal Flag', date: '3 days ago', sentiment: 'risk', summary: 'System detected a 12% gap between input tax credit claimed and supplier filings for Q3.' }
] as any

const ratios = [
  { label: 'Current Ratio', value: '1.45', trend: 'up', unit: 'x', description: 'Ability to pay short-term obligations.' },
  { label: 'Debt to Equity', value: '0.42', trend: 'down', unit: '', description: 'Measure of financial leverage.' },
  { label: 'ICR', value: '4.2', trend: 'up', unit: 'x', description: 'Interest Coverage Ratio: Earnings relative to interest expense.' },
  { label: 'DSCR', value: '1.82', trend: 'stable', unit: 'x', description: 'Debt Service Coverage Ratio: Cash available for debt servicing.' }
] as any
</script>

<template>
  <div class="space-y-8 pb-20">
    <!-- Case Header -->
    <header class="flex items-center justify-between bg-slate-900 border border-slate-800 p-8 rounded-3xl shadow-xl">
      <div class="flex items-center gap-8">
        <ScoreGauge :score="82" :size="120" />
        <div>
          <div class="flex items-center gap-3 mb-2">
            <h1 class="text-3xl font-black text-white">Tata Steel Ltd</h1>
            <span class="px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-[10px] font-bold uppercase tracking-widest">Low Risk</span>
          </div>
          <div class="grid grid-cols-2 gap-x-6 gap-y-1 text-xs text-slate-500 font-medium">
            <p>CIN: <span class="text-slate-300">L27100MH1907PLC000260</span></p>
            <p>Sectors: <span class="text-slate-300">Steel / Infrastructure</span></p>
            <p>Established: <span class="text-slate-300">1907</span></p>
            <p>Rating: <span class="text-slate-300">AA+ (Stable)</span></p>
          </div>
        </div>
      </div>
      <div class="flex gap-4">
        <button class="px-5 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-sm font-bold rounded-xl transition-colors">
          Export Raw Data
        </button>
        <button @click="$router.push(`/case/${$route.params.id}/cam`)" class="px-5 py-2.5 bg-blue-600 hover:bg-blue-700 text-white text-sm font-bold rounded-xl transition-colors shadow-lg shadow-blue-500/20">
          View CAM Document
        </button>
      </div>
    </header>

    <!-- Navigation Tabs -->
    <nav class="flex items-center p-1.5 bg-slate-900 border border-slate-800 rounded-2xl w-max">
      <button 
        v-for="tab in ['financials', 'research', 'qualitative', 'scoring']" 
        :key="tab"
        @click="activeTab = tab"
        class="px-8 py-2.5 rounded-xl text-sm font-bold capitalize transition-all"
        :class="activeTab === tab ? 'bg-slate-800 text-blue-400 shadow-sm' : 'text-slate-500 hover:text-slate-300'"
      >
        {{ tab }}
      </button>
    </nav>

    <!-- Tab Content -->
    <transition name="fade" mode="out-in">
      <div v-if="activeTab === 'financials'" key="financials" class="space-y-8">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <FinancialRatioCard v-for="ratio in ratios" :key="ratio.label" v-bind="ratio" />
        </div>
        <div class="bg-slate-900 border border-slate-800 p-8 rounded-3xl">
          <h3 class="text-lg font-bold text-white mb-6">Historical Performance</h3>
          <div class="h-64 flex items-end gap-1 px-4">
             <div v-for="i in 12" :key="i" class="flex-1 bg-blue-500/20 rounded-t-lg relative group transition-all hover:bg-blue-500/40" :style="{ height: (30 + Math.random() * 70) + '%' }">
                <div class="absolute -top-10 left-1/2 -translate-x-1/2 bg-slate-800 text-white text-[10px] py-1 px-2 rounded opacity-0 group-hover:opacity-100 transition-opacity">₹ {{(Math.random()*100).toFixed(1)}} Cr</div>
             </div>
          </div>
          <div class="flex justify-between mt-4 px-2 text-[10px] font-bold text-slate-600 uppercase tracking-widest">
            <span>Apr 2025</span>
            <span>Mar 2026</span>
          </div>
        </div>
      </div>

      <div v-else-if="activeTab === 'research'" key="research" class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div class="lg:col-span-2">
           <div class="bg-slate-900 border border-slate-800 rounded-3xl p-8">
             <h3 class="text-lg font-bold text-white mb-6">Intelligence Feed</h3>
             <ResearchFeed :items="newsItems" />
           </div>
        </div>
        <div class="space-y-8">
           <div class="bg-slate-900 border border-slate-800 rounded-3xl p-6">
             <h4 class="text-sm font-bold text-slate-500 uppercase tracking-widest mb-6">Sentiment Analysis</h4>
             <div class="flex items-center justify-between mb-4">
                <span class="text-emerald-400 text-sm font-bold leading-none">68% Positive</span>
                <span class="text-red-400 text-sm font-bold leading-none">12% Negative</span>
             </div>
             <div class="h-2 w-full bg-slate-800 rounded-full overflow-hidden flex">
                <div class="h-full bg-emerald-500" style="width: 68%"></div>
                <div class="h-full bg-slate-600" style="width: 20%"></div>
                <div class="h-full bg-red-500" style="width: 12%"></div>
             </div>
           </div>
           
           <div class="bg-slate-900 border border-slate-800 rounded-3xl p-6">
             <h4 class="text-sm font-bold text-slate-500 uppercase tracking-widest mb-6">Legal Watch</h4>
             <div class="space-y-4">
                <div class="flex items-center justify-between p-3 bg-slate-950 rounded-xl border border-slate-800">
                   <div class="text-xs font-bold text-slate-300">NCLT Actions</div>
                   <div class="text-xs font-black text-emerald-500">CLEAR</div>
                </div>
                <div class="flex items-center justify-between p-3 bg-slate-950 rounded-xl border border-slate-800">
                   <div class="text-xs font-bold text-slate-300">Active Litigation</div>
                   <div class="text-xs font-black text-amber-500">2 FOUND</div>
                </div>
             </div>
           </div>
        </div>
      </div>

      <div v-else-if="activeTab === 'qualitative'" key="qualitative">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
           <div class="bg-slate-900 border border-slate-800 rounded-3xl p-8">
             <h3 class="text-lg font-bold text-white mb-8">Primary Due Diligence</h3>
             <div class="space-y-8">
                <div v-for="q in [
                  {l:'Management Integrity', v:'High', d:'Promoters have strong market reputation and no history of defaults.'},
                  {l:'Operational Efficiency', v:'Good', d:'Plant utilization at 82% over the last two quarters.'},
                  {l:'Collateral Quality', v:'Standard', d:'Industrial land with residential conversion potential.'}
                ]" :key="q.l" class="pb-6 border-b border-slate-800 last:border-0">
                   <div class="flex items-center justify-between mb-2">
                      <span class="text-sm font-bold text-slate-200">{{ q.l }}</span>
                      <span class="px-2 py-0.5 rounded-lg bg-blue-500/10 text-blue-400 text-[10px] font-black uppercase">{{ q.v }}</span>
                   </div>
                   <p class="text-xs text-slate-500 italic">"{{ q.d }}"</p>
                </div>
             </div>
           </div>
           <div class="bg-blue-600/5 border border-blue-500/10 rounded-3xl p-8">
              <h3 class="text-lg font-bold text-blue-400 mb-6">Recommended Adjustments</h3>
              <p class="text-sm text-slate-400 mb-8">System-calculated override based on qualitative inputs.</p>
              <div class="space-y-3">
                 <div class="flex items-center justify-between p-4 bg-slate-900 rounded-2xl border border-slate-800">
                    <span class="text-sm font-bold text-slate-300">Management Alpha</span>
                    <span class="text-emerald-400 font-bold">+4 pts</span>
                 </div>
                 <div class="flex items-center justify-between p-4 bg-slate-900 rounded-2xl border border-slate-800 opacity-50">
                    <span class="text-sm font-bold text-slate-300">Sector Headwinds</span>
                    <span class="text-red-400 font-bold">-2 pts</span>
                 </div>
              </div>
           </div>
        </div>
      </div>

      <div v-else-if="activeTab === 'scoring'" key="scoring" class="space-y-8">
         <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div class="bg-slate-900 border border-slate-800 rounded-3xl p-8 flex flex-col items-center">
               <h3 class="text-lg font-bold text-white mb-10 w-full">Final Scoring Recommendation</h3>
               <ScoreGauge :score="82" :size="200" />
               <div class="mt-8 text-center">
                  <p class="text-4xl font-black text-emerald-400 mb-2">APPROVE</p>
                  <p class="text-sm text-slate-500">Recommended Limit: <span class="text-slate-100 font-bold">₹ 450 Cr</span></p>
               </div>
            </div>
            <div class="bg-slate-900 border border-slate-800 rounded-3xl p-8">
               <h3 class="text-lg font-bold text-white mb-6">SHAP Explainability Waterfall</h3>
               <p class="text-xs text-slate-500 mb-8">Feature contribution to final default probability score.</p>
               <div class="space-y-4">
                  <div v-for="f in [
                    {n:'ICR', v:'+12.4', p:true},
                    {n:'Sector Performance', v:'+8.1', p:true},
                    {n:'Recent News Sentiment', v:'+3.2', p:true},
                    {n:'D/E Ratio', v:'-2.5', p:false},
                    {n:'Litigation Risk', v:'-5.8', p:false}
                  ]" :key="f.n" class="flex items-center gap-4">
                     <span class="w-32 text-[10px] font-bold text-slate-400 uppercase tracking-widest">{{ f.n }}</span>
                     <div class="flex-1 h-3 bg-slate-800 rounded-full overflow-hidden relative">
                        <div 
                          class="absolute h-full rounded-full transition-all duration-1000" 
                          :class="f.p ? 'bg-emerald-500 right-1/2' : 'bg-red-500 left-1/2'"
                          :style="{ width: (Math.abs(parseFloat(f.v)) * 4) + '%'}"
                        ></div>
                     </div>
                     <span class="w-12 text-[10px] font-black" :class="f.p ? 'text-emerald-500' : 'text-red-500'">{{ f.v }}</span>
                  </div>
               </div>
               <div class="mt-12 p-4 bg-slate-950 rounded-2xl border border-slate-800">
                  <p class="text-xs text-slate-400 leading-relaxed">
                    <span class="font-bold text-blue-400 italic">Decision Rationale:</span> Approved due to exceptional Interest Coverage Ratio (4.2x) and positive news sentiment, which offset the moderate litigation risk identified in the news feed.
                  </p>
               </div>
            </div>
         </div>
      </div>
    </transition>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
