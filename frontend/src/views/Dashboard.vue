<script setup lang="ts">
import { computed } from 'vue'
import { 
  Plus, 
  ArrowRight, 
  Activity, 
  Percent, 
  ShieldAlert, 
  CheckCircle2,
  Clock,
  ExternalLink,
  Loader2
} from 'lucide-vue-next'
import { useCollection } from 'vuefire'
import { collection, query, orderBy, limit } from 'firebase/firestore'
import { db } from '../firebase'
import ScoreGauge from '../components/ScoreGauge.vue'

// Real-time cases for stats calculation (fetch more for better accuracy)
const allCasesQuery = query(collection(db, 'cases'), orderBy('date', 'desc'), limit(100))
const allCases = useCollection(allCasesQuery)

// Real-time cases for the recent list
const casesQuery = query(collection(db, 'cases'), orderBy('date', 'desc'), limit(10))
const recentCases = useCollection(casesQuery)

const formatCurrency = (value: number) => {
  if (value >= 100) return `₹ ${(value / 100).toFixed(1)}B`
  return `₹ ${value}Cr`
}

// Compute stats dynamically
const stats = computed(() => {
  const cases = allCases.value || []
  const activeCount = cases.length
  const avgScore = cases.length > 0 
    ? Math.round(cases.reduce((acc, c) => acc + (c.score || 0), 0) / cases.length) 
    : 0
  const highRiskCount = cases.filter(c => (c.score || 0) < 50).length
  
  // Summing limits for "Approved" (mocking limit for now if not in document)
  const totalApproved = cases
    .filter(c => c.status === 'Approved' || c.status === 'COMPLETE')
    .reduce((acc, c) => acc + (parseFloat(c.limit) || 0), 0)
  
  return [
    { label: 'Active Cases', value: activeCount.toString(), icon: Activity },
    { label: 'Avg Score', value: avgScore.toString(), icon: Percent },
    { label: 'High Risk', value: highRiskCount.toString(), icon: ShieldAlert },
    { label: 'Approved', value: totalApproved > 0 ? formatCurrency(totalApproved) : '₹ 0Cr', icon: CheckCircle2 },
  ]
})
</script>

<template>
  <div class="space-y-12 pb-20">
    <!-- Header Section -->
    <header class="flex items-end justify-between px-2">
      <div>
        <h1 class="text-4xl font-black text-[var(--text-heading)] tracking-tight">Credit Portfolio</h1>
        <p class="text-[var(--text-muted)] mt-2 text-lg font-medium">Real-time credit appraisal monitoring engine.</p>
      </div>
      <router-link to="/case/new" class="group relative px-6 py-3 bg-primary rounded-2xl overflow-hidden transition-all hover:scale-105 active:scale-95 shadow-xl shadow-primary/20">
        <div class="absolute inset-0 bg-gradient-to-r from-white/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
        <span class="relative flex items-center gap-2 text-white font-black uppercase tracking-wider text-sm">
          <Plus class="w-5 h-5" />
          Initiate Appraisal
        </span>
      </router-link>
    </header>

    <!-- Quick Stats -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
      <div v-for="stat in stats" :key="stat.label"
           class="p-8 bg-[var(--surface-raised)] border border-[var(--border-main)] rounded-[2rem] shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all group">
        <div class="flex items-start justify-between mb-4">
          <p class="text-[10px] font-black text-[var(--text-label)] uppercase tracking-[0.2em]">{{ stat.label }}</p>
          <div class="w-8 h-8 rounded-lg bg-primary/5 flex items-center justify-center text-[var(--text-muted)] group-hover:text-primary group-hover:bg-primary/10 transition-all">
            <component :is="stat.icon" class="w-4 h-4" />
          </div>
        </div>
        <div v-if="!recentCases" class="h-10 w-24 bg-[var(--surface-1)] animate-pulse rounded-lg"></div>
        <p v-else class="text-4xl font-black text-[var(--text-heading)] tracking-tighter">{{ stat.value }}</p>
      </div>
    </div>

    <!-- Case Grid -->
    <section>
      <div class="flex items-center justify-between mb-8 px-2">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-primary/10 text-primary flex items-center justify-center">
            <Clock class="w-6 h-6" />
          </div>
          <h2 class="text-2xl font-black text-[var(--text-heading)] tracking-tight">Recent Appraisals</h2>
        </div>
        <button class="flex items-center gap-2 text-xs font-black text-primary hover:text-primary-hover transition-all group uppercase tracking-widest bg-primary/5 px-4 py-2 rounded-xl border border-primary/10 hover:border-primary/30">
          View Archive 
          <ArrowRight class="w-4 h-4 transform group-hover:translate-x-1 transition-transform" />
        </button>
      </div>
      
      <!-- Loading State -->
      <div v-if="!recentCases" class="flex flex-col items-center justify-center py-20 bg-[var(--surface-raised)] rounded-[3rem] border border-[var(--border-main)] border-dashed">
        <Loader2 class="w-12 h-12 text-primary animate-spin mb-4" />
        <p class="text-[var(--text-muted)] font-black uppercase tracking-widest text-xs">Syncing with engine...</p>
      </div>

      <!-- Empty State -->
      <div v-else-if="recentCases.length === 0" class="flex flex-col items-center justify-center py-24 bg-[var(--surface-raised)] rounded-[3rem] border border-[var(--border-main)] border-dashed">
         <div class="w-20 h-20 rounded-[2rem] bg-[var(--surface-1)] flex items-center justify-center mb-6">
            <Clock class="w-10 h-10 text-[var(--text-muted)] opacity-30" />
         </div>
         <h3 class="text-xl font-black text-[var(--text-heading)] mb-2">No active appraisals</h3>
         <p class="text-[var(--text-muted)] font-medium">Initiate a new case to start the AI analysis pipeline.</p>
         <router-link to="/case/new" class="mt-8 px-8 py-3 bg-primary text-white text-xs font-black rounded-xl uppercase tracking-widest hover:scale-105 active:scale-95 transition-all">
            New Appraisal
         </router-link>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4 gap-10">
        <div v-for="caseItem in recentCases" :key="caseItem.id" 
             class="group bg-[var(--surface-raised)] border border-[var(--border-main)] rounded-[2.5rem] p-10 transition-all hover:border-primary/30 hover:shadow-2xl hover:shadow-primary/5 cursor-pointer relative overflow-hidden"
             @click="$router.push(`/case/${caseItem.id}`)">
          
          <div class="absolute top-0 right-0 p-8 opacity-0 group-hover:opacity-100 transition-all group-hover:scale-110">
            <ExternalLink class="w-5 h-5 text-[var(--text-muted)] hover:text-primary" />
          </div>

          <div class="flex flex-col items-center">
            <ScoreGauge :score="caseItem.score" :size="180" />
            <div class="mt-10 text-center">
              <h3 class="text-2xl font-black text-[var(--text-heading)] group-hover:text-primary transition-colors leading-tight tracking-tight">{{ caseItem.name }}</h3>
              <div class="flex items-center gap-2 justify-center mt-4">
                <span class="text-[10px] font-black px-3 py-1.5 rounded-lg bg-[var(--surface-1)] text-[var(--text-label)] border border-[var(--border-main)] uppercase tracking-[0.1em]">
                  {{ caseItem.status }}
                </span>
                <span class="text-[11px] font-black text-[var(--text-muted)] uppercase tracking-tighter">{{ caseItem.date }}</span>
              </div>
            </div>
          </div>
          
          <div class="mt-12 pt-10 border-t border-[var(--border-main)] grid grid-cols-2 gap-10">
             <div class="text-center group-hover:scale-105 transition-transform">
               <p class="text-[10px] font-black text-[var(--text-muted)] uppercase tracking-[0.2em] mb-2">DSCR</p>
               <p class="text-xl font-black text-[var(--text-heading)] tracking-tighter">{{ caseItem.dscr }}</p>
             </div>
             <div class="text-center group-hover:scale-105 transition-transform">
               <p class="text-[10px] font-black text-[var(--text-muted)] uppercase tracking-[0.2em] mb-2">D/E Ratio</p>
               <p class="text-xl font-black text-[var(--text-heading)] tracking-tighter">{{ caseItem.de }}</p>
             </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
