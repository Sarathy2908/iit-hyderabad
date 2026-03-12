<script setup lang="ts">
import ScoreGauge from '../components/ScoreGauge.vue'

const recentCases = [
  { id: '1', name: 'Tata Steel Ltd', score: 82, status: 'Complete', date: '2026-03-11' },
  { id: '2', name: 'Adani Green Energy', score: 45, status: 'Scoring', date: '2026-03-12' },
  { id: '3', name: 'Reliance Industries', score: 91, status: 'Complete', date: '2026-03-10' },
]
</script>

<template>
  <div class="space-y-12 pb-20">
    <!-- Header Section -->
    <header class="flex items-end justify-between">
      <div>
        <h1 class="text-4xl font-black text-white tracking-tight">Credit Portfolio</h1>
        <p class="text-slate-400 mt-2 text-lg">Real-time credit appraisal monitoring engine.</p>
      </div>
      <router-link to="/case/new" class="group relative px-6 py-3 bg-blue-600 rounded-xl overflow-hidden transition-all hover:scale-105 active:scale-95 shadow-lg shadow-blue-500/20">
        <div class="absolute inset-0 bg-gradient-to-r from-blue-400/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
        <span class="relative flex items-center gap-2 text-white font-bold">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
          Initiate Appraisal
        </span>
      </router-link>
    </header>

    <!-- Quick Stats -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <div v-for="stat in [{l:'Active Cases', v:'12'}, {l:'Avg Score', v:'74'}, {l:'High Risk', v:'3'}, {l:'Approved', v:'$1.2B'}]" 
           class="p-6 bg-slate-900/50 border border-slate-800 rounded-2xl backdrop-blur-sm">
        <p class="text-[10px] font-black text-slate-500 uppercase tracking-[0.2em] mb-1">{{ stat.l }}</p>
        <p class="text-3xl font-bold text-white">{{ stat.v }}</p>
      </div>
    </div>

    <!-- Case Grid -->
    <section>
      <div class="flex items-center justify-between mb-8">
        <h2 class="text-xl font-bold text-slate-200">Recent Appraisals</h2>
        <button class="text-sm font-semibold text-blue-400 hover:text-blue-300 transition-colors">View All Archive →</button>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div v-for="caseItem in recentCases" :key="caseItem.id" 
             class="group bg-slate-900 border border-slate-800 rounded-3xl p-6 transition-all hover:border-slate-700 hover:shadow-2xl hover:shadow-blue-500/5 cursor-pointer"
             @click="$router.push(`/case/${caseItem.id}`)">
          <div class="flex flex-col items-center">
            <ScoreGauge :score="caseItem.score" :size="160" />
            <div class="mt-6 text-center">
              <h3 class="text-xl font-bold text-white group-hover:text-blue-400 transition-colors">{{ caseItem.name }}</h3>
              <div class="flex items-center gap-2 justify-center mt-2">
                <span class="text-[11px] font-bold px-2 py-0.5 rounded-full bg-slate-800 text-slate-400 border border-slate-700 uppercase">{{ caseItem.status }}</span>
                <span class="text-[11px] font-medium text-slate-600">{{ caseItem.date }}</span>
              </div>
            </div>
          </div>
          <div class="mt-8 pt-6 border-t border-slate-800 grid grid-cols-2 gap-4">
             <div class="text-center">
               <p class="text-[9px] font-bold text-slate-500 uppercase tracking-widest">DSCR</p>
               <p class="text-sm font-bold text-slate-300">1.8x</p>
             </div>
             <div class="text-center">
               <p class="text-[9px] font-bold text-slate-500 uppercase tracking-widest">D/E Ratio</p>
               <p class="text-sm font-bold text-slate-300">0.42</p>
             </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
