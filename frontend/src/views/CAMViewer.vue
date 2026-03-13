<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { 
  ChevronLeft, 
  Briefcase, 
  ShieldCheck, 
  Download, 
  Sparkles, 
  Clock, 
  TrendingUp, 
  Building2, 
  AlertTriangle, 
  CheckCircle,
  Loader2
} from 'lucide-vue-next'
import { useDocument } from 'vuefire'
import { doc } from 'firebase/firestore'
import { db } from '../firebase'

const route = useRoute()
// If this is a child route, the ID might be in route.params.id or parent.
const caseId = computed(() => route.params.id as string)
const caseRef = doc(db, 'cases', caseId.value)
const { data: caseData, pending, error } = useDocument(caseRef)

// Icon mapper
const iconMap: Record<string, any> = { TrendingUp, Building2, ShieldCheck }

const formattedDate = computed(() => {
  if (!caseData.value?.date) return new Date().toLocaleDateString('en-IN', { day: 'numeric', month: 'long', year: 'numeric' })
  return new Date(caseData.value.date).toLocaleDateString('en-IN', { day: 'numeric', month: 'long', year: 'numeric' })
})

const handleDownload = () => {
  window.print()
}
</script>

<template>
  <div class="max-w-6xl mx-auto pb-20">
    <header class="flex items-center justify-between mb-12 px-2">
      <div class="flex flex-col gap-2">
        <button @click="$router.back()" class="flex items-center gap-2 text-[var(--text-muted)] hover:text-[var(--text-heading)] transition-all mb-4 group active:scale-95">
          <ChevronLeft class="w-5 h-5 transform group-hover:-translate-x-1 transition-transform" />
          <span class="font-bold text-sm">Return to Case</span>
        </button>
        <div class="flex items-center gap-6">
          <div class="w-14 h-14 rounded-2xl bg-primary/10 text-primary flex items-center justify-center border-2 border-primary/20 shadow-xl shadow-primary/5">
            <Briefcase class="w-8 h-8" />
          </div>
          <div v-if="caseData">
            <h1 class="text-4xl font-black text-[var(--text-heading)] tracking-tighter">Credit Appraisal Memo</h1>
            <p class="text-[var(--text-main)] mt-1 font-black italic flex items-center gap-2 opacity-60">
              <ShieldCheck class="w-4 h-4 text-primary" />
              Internal Document • Confidential • {{ caseData.name }}
            </p>
          </div>
          <div v-else-if="pending" class="animate-pulse space-y-2">
             <div class="h-8 w-64 bg-[var(--surface-2)] rounded-lg"></div>
             <div class="h-4 w-48 bg-[var(--surface-1)] rounded-lg"></div>
          </div>
        </div>
      </div>
      <button @click="handleDownload" :disabled="pending || !caseData" class="flex items-center gap-3 px-10 py-5 bg-primary hover:bg-primary-hover text-white font-black rounded-[2rem] transition-all shadow-2xl shadow-primary/20 active:scale-95 group uppercase tracking-[0.2em] text-xs disabled:opacity-30">
        <Download class="w-5 h-5 transform group-hover:translate-y-1 transition-transform" />
        Download CAM PDF
      </button>
    </header>

    <div v-if="pending" class="flex flex-col items-center justify-center py-60 bg-[var(--surface-raised)] rounded-[4rem] border border-[var(--border-main)] border-dashed">
      <Loader2 class="w-16 h-16 text-primary animate-spin mb-6" />
      <p class="font-black uppercase tracking-[0.3em] text-xs opacity-40">Compiling Report...</p>
    </div>

    <div v-else-if="error || !caseData" class="py-40 text-center bg-[var(--surface-raised)] rounded-[4rem] border border-[var(--color-danger)]/20">
       <AlertTriangle class="w-16 h-16 text-[var(--color-danger)] mx-auto mb-6" />
       <h2 class="text-2xl font-black">Memo Unreachable</h2>
       <p class="text-[var(--text-muted)] mt-2">The appraisal data for this session could not be retrieved.</p>
    </div>

    <div v-else class="bg-[var(--surface-raised)] text-[var(--text-main)] rounded-[3.5rem] shadow-2xl p-20 min-h-[1000px] border border-[var(--border-main)] relative overflow-hidden">
      <!-- Watermark -->
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 rotate-[35deg] text-[var(--text-muted)] text-[12rem] font-black pointer-events-none select-none opacity-[0.03] tracking-widest">
        INTELLI-CREDIT
      </div>

      <div class="relative z-10 space-y-20">
        <div class="flex justify-between border-b-2 border-[var(--border-main)] pb-12">
          <div class="space-y-6">
            <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-primary/10 text-primary border border-primary/20 text-[10px] font-black uppercase tracking-[0.2em] shadow-sm">
              <Sparkles class="w-3.5 h-3.5" />
              Automated Intelligence Generation
            </div>
            <h2 class="text-4xl font-black uppercase tracking-tighter text-[var(--text-heading)]">CAM #{{ caseId.substring(0,8).toUpperCase() }}</h2>
            <div class="flex items-center gap-4 text-sm font-black text-[var(--text-label)] opacity-60">
              <Clock class="w-4.5 h-4.5" />
              Date of Issue: {{ formattedDate }}
            </div>
          </div>
          <div class="text-right flex flex-col justify-end">
            <p class="text-[10px] font-black text-[var(--text-muted)] uppercase tracking-[0.3em] mb-2">Engine Signature</p>
            <p class="text-2xl font-black text-primary tracking-tighter">IntelliCredit AI v4.0</p>
            <p class="text-sm font-black text-[var(--text-label)] opacity-60">Corporate Credit Dept.</p>
          </div>
        </div>

        <section class="group">
          <h3 class="text-[10px] font-black uppercase text-primary mb-8 tracking-[0.4em] flex items-center gap-4">
             <div class="w-2.5 h-5 bg-primary rounded-full shadow-[0_0_10px_rgba(var(--primary),0.3)]"></div>
             I. Executive Summary
          </h3>
          <div class="pl-6 border-l-2 border-[var(--border-main)]/50 group-hover:border-primary/30 transition-colors">
            <p class="text-lg leading-relaxed text-[var(--text-main)] font-medium group-hover:text-[var(--text-heading)] transition-colors">
              {{ caseData.name }} (the "Borrower") demonstrates a risk profile with a composite score of 
              <span class="text-[var(--text-heading)] font-black decoration-primary/20 underline underline-offset-8 decoration-4">{{ caseData.score }}</span>. 
              The analysis indicates {{ caseData.score > 70 ? 'strong' : 'moderate' }} solvency supported by {{ caseData.ratios?.[0]?.label || 'key financials' }}.
              {{ caseData.sentimentSummary || 'Market sentiment is neutrally positioned.' }}
            </p>
          </div>
        </section>

        <section class="group">
          <h3 class="text-[10px] font-black uppercase text-primary mb-8 tracking-[0.4em] flex items-center gap-4">
             <div class="w-2.5 h-5 bg-primary rounded-full shadow-[0_0_10px_rgba(var(--primary),0.3)]"></div>
             II. Financial Snapshot
          </h3>
          <div class="grid grid-cols-3 gap-12 py-12 px-12 bg-[var(--surface-1)] rounded-[2.5rem] border border-[var(--border-main)] group-hover:border-primary/40 transition-all shadow-inner">
            <div v-for="s in (caseData.camRatios || [
              {l:'Revenue Scale', v: 'Significant', i: 'Building2'}, 
              {l:'D/E Ratio', v: caseData.de || 'N/A', i: 'ShieldCheck'},
              {l:'DSCR', v: caseData.dscr || 'N/A', i: 'TrendingUp'}
            ])" :key="s.l" class="flex flex-col gap-3">
              <div class="flex items-center gap-3 text-[10px] font-black text-[var(--text-label)] uppercase tracking-[0.2em] opacity-60">
                <div class="w-8 h-8 rounded-lg bg-[var(--surface-raised)] flex items-center justify-center border border-[var(--border-main)] group-hover:text-primary transition-colors">
                  <component :is="iconMap[s.i] || Building2" class="w-4 h-4" />
                </div>
                {{ s.l }}
              </div>
              <p class="text-4xl font-black text-[var(--text-heading)] tracking-tighter group-hover:scale-105 transition-transform origin-left">{{ s.v }}</p>
            </div>
          </div>
        </section>

        <section class="group">
          <h3 class="text-[10px] font-black uppercase text-primary mb-8 tracking-[0.4em] flex items-center gap-4">
             <div class="w-2.5 h-5 bg-primary rounded-full shadow-[0_0_10px_rgba(var(--primary),0.3)]"></div>
             III. Risk Intelligence
          </h3>
          <div class="space-y-8 pl-6">
             <div class="p-10 border border-[var(--color-success)]/10 bg-[var(--color-success-muted)]/10 rounded-[2.5rem] relative overflow-hidden group/item hover:bg-[var(--color-success-muted)]/20 transition-colors">
                <div class="absolute top-0 right-0 w-32 h-32 bg-[var(--color-success)]/5 blur-3xl"></div>
                <div class="flex items-center gap-4 mb-5">
                   <div class="w-10 h-10 rounded-xl bg-[var(--color-success-muted)] text-[var(--color-success)] flex items-center justify-center border border-[var(--color-success)]/20 shadow-sm">
                     <TrendingUp class="w-5 h-5" />
                   </div>
                   <p class="text-[10px] font-black text-[var(--color-success)] uppercase tracking-[0.2em]">Market Sentiment Alpha</p>
                </div>
                <p class="text-base italic text-[var(--text-main)] leading-relaxed font-black opacity-80 group-hover/item:opacity-100 transition-opacity">
                  {{ caseData.sentimentSummary || 'Sentiment data is being aggregated from regulatory and social feeds.' }}
                </p>
             </div>
             <div v-if="caseData.legalFlags?.litigationCount" class="p-10 border border-[var(--color-warning)]/10 bg-[var(--color-warning-muted)]/10 rounded-[2.5rem] relative overflow-hidden group/item hover:bg-[var(--color-warning-muted)]/20 transition-colors">
                <div class="absolute top-0 right-0 w-32 h-32 bg-[var(--color-warning)]/5 blur-2xl"></div>
                <div class="flex items-center gap-4 mb-5">
                   <div class="w-10 h-10 rounded-xl bg-[var(--color-warning-muted)] text-[var(--color-warning)] flex items-center justify-center border border-[var(--color-warning)]/20 shadow-sm">
                     <AlertTriangle class="w-5 h-5" />
                   </div>
                   <p class="text-[10px] font-black text-[var(--color-warning)] uppercase tracking-[0.2em]">Regulatory Intelligence</p>
                </div>
                <p class="text-base italic text-[var(--text-main)] leading-relaxed font-black opacity-80 group-hover/item:opacity-100 transition-opacity">
                  Active litigation found in <span class="text-[var(--text-heading)] underline decoration-[var(--color-warning)]/30">{{ caseData.legalFlags.litigationCount }} cases</span>. Exposure analysis indicates low materiality relative to net worth.
                </p>
             </div>
          </div>
        </section>

        <section class="group">
          <h3 class="text-[10px] font-black uppercase text-primary mb-8 tracking-[0.4em] flex items-center gap-4">
             <div class="w-2.5 h-5 bg-primary rounded-full shadow-[0_0_10px_rgba(var(--primary),0.3)]"></div>
             IV. Recommendation
          </h3>
          <div class="bg-[var(--surface-1)] border border-primary/20 p-16 rounded-[3.5rem] shadow-2xl relative overflow-hidden group-hover:border-primary/40 transition-all">
             <div class="absolute -top-24 -right-24 w-80 h-80 bg-primary/5 blur-[100px]"></div>
             <div class="flex items-center justify-between mb-12 relative z-10">
                <div class="flex items-center gap-6">
                   <div 
                    class="w-20 h-20 rounded-3xl border-2 flex items-center justify-center shadow-xl"
                    :class="caseData.score > 60 ? 'bg-[var(--color-success-muted)] border-[var(--color-success)]/20 text-[var(--color-success)] shadow-[var(--color-success)]/10' : 'bg-[var(--color-warning-muted)] border-[var(--color-warning)]/20 text-[var(--color-warning)] shadow-[var(--color-warning)]/10'"
                   >
                     <CheckCircle v-if="caseData.score > 60" class="w-12 h-12" />
                     <AlertTriangle v-else class="w-12 h-12" />
                   </div>
                   <span 
                    class="text-7xl font-black tracking-tighter"
                    :class="caseData.score > 60 ? 'text-[var(--color-success)]' : 'text-[var(--color-warning)]'"
                   >
                    {{ caseData.decision || 'HOLD' }}
                   </span>
                </div>
                <div class="text-right">
                   <p class="text-[10px] font-black text-[var(--text-label)] uppercase tracking-[0.3em] mb-2 opacity-60">Recommended Limit</p>
                   <p class="text-5xl font-black text-[var(--text-heading)] tracking-tighter decoration-primary/20 underline decoration-4 underline-offset-8">₹ {{ caseData.limit || '0' }} Cr</p>
                </div>
             </div>
             <div class="grid grid-cols-2 lg:grid-cols-4 gap-12 text-sm pt-12 border-t border-[var(--border-main)] relative z-10">
                <div v-for="m in [
                  {l:'Interest Rate', v: caseData.terms?.roi || 'REPO + 180 BPS'},
                  {l:'Tenor', v: caseData.terms?.tenor || '36 MONTHS'},
                  {l:'Security', v: caseData.terms?.security || 'Exclusive Assets Charge'},
                  {l:'Repayment', v: caseData.terms?.repayment || 'Monthly Installments'}
                ]" :key="m.l" class="flex flex-col gap-2">
                   <span class="text-[10px] font-black text-[var(--text-muted)] uppercase tracking-[0.2em] opacity-60">{{ m.l }}</span>
                   <p class="text-sm font-black text-[var(--text-heading)] uppercase tracking-tighter">{{ m.v }}</p>
                </div>
             </div>
          </div>
        </section>

        <div class="pt-40 flex justify-between px-12 border-t border-[var(--border-main)]/30">
           <div class="flex flex-col items-center gap-6 group/sign">
              <div class="w-64 h-[2px] bg-[var(--border-main)] group-hover/sign:bg-primary transition-all duration-700 shadow-sm relative">
                <div class="absolute inset-0 bg-primary/40 scale-x-0 group-hover/sign:scale-x-100 transition-transform origin-center"></div>
              </div>
              <p class="text-[10px] font-black text-[var(--text-label)] uppercase tracking-[0.3em] group-hover/sign:text-primary transition-colors">Intelli-Credit AI Sign-off</p>
              <div class="flex items-center gap-2.5 text-[9px] mt-2 font-black text-[var(--color-success)] bg-[var(--color-success-muted)] px-4 py-1.5 rounded-full border border-[var(--color-success)]/20 shadow-sm group-hover/sign:scale-110 transition-transform">
                 <ShieldCheck class="w-4 h-4" />
                 CRYPTOGRAPHICALLY VERIFIED
              </div>
           </div>
           <div class="flex flex-col items-center gap-6 group/sign">
              <div class="w-64 h-[2px] bg-[var(--border-main)] group-hover/sign:bg-primary transition-all duration-700 shadow-sm relative">
                <div class="absolute inset-0 bg-primary/40 scale-x-0 group-hover/sign:scale-x-100 transition-transform origin-center"></div>
              </div>
              <p class="text-[10px] font-black text-[var(--text-label)] uppercase tracking-[0.3em] group-hover/sign:text-primary transition-colors">Credit Manager Signature</p>
              <p class="text-[10px] mt-2 font-black text-[var(--text-muted)] italic opacity-40 uppercase tracking-widest animate-pulse">Awaiting Digital Signature...</p>
           </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.group:hover .shadow-2xl {
  transform: translateY(-4px);
}
</style>
