<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { 
  ChevronLeft,
  Download,
  FileText,
  TrendingUp,
  TrendingDown,
  AlertTriangle,
  CheckCircle,
  BarChart3,
  Search,
  MessageSquare,
  Gauge,
  Sparkles,
  Activity,
  ShieldCheck,
  Quote,
  Zap,
  Loader2
} from 'lucide-vue-next'
import { useDocument } from 'vuefire'
import { doc } from 'firebase/firestore'
import { db } from '../firebase'
import ScoreGauge from '../components/ScoreGauge.vue'
import FinancialRatioCard from '../components/FinancialRatioCard.vue'
import ResearchFeed from '../components/ResearchFeed.vue'

const route = useRoute()
const activeTab = ref('financials')

// Dynamic case document from Firestore
const caseRef = doc(db, 'cases', route.params.id as string)
const { data: caseData, pending, error } = useDocument(caseRef)

// Map dynamic data or fallback to defaults
const newsItems = computed(() => caseData.value?.newsItems || [])
const ratios = computed(() => caseData.value?.ratios || [])

function exportRawData() {
  if (!caseData.value) return
  const dataStr = JSON.stringify(caseData.value, null, 2)
  const dataBlob = new Blob([dataStr], { type: 'application/json' })
  const url = URL.createObjectURL(dataBlob)
  const link = document.createElement('a')
  link.href = url
  link.download = `case_${caseData.value.name.replace(/\s+/g, '_')}_data.json`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
}
</script>
<template>
  <div class="space-y-8 pb-20">
    <div class="px-2">
      <button @click="$router.back()" class="flex items-center gap-2 text-[var(--text-muted)] hover:text-[var(--text-heading)] transition-all mb-4 group active:scale-95">
        <ChevronLeft class="w-5 h-5 transform group-hover:-translate-x-1 transition-transform" />
        <span class="font-bold text-sm">Back to Dashboard</span>
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="pending" class="flex flex-col items-center justify-center py-40 bg-[var(--surface-raised)] rounded-[3rem] border border-[var(--border-main)] border-dashed">
      <Loader2 class="w-16 h-16 text-primary animate-spin mb-6" />
      <h2 class="text-2xl font-black text-[var(--text-heading)] animate-pulse">Syncing Case Data...</h2>
      <p class="text-[var(--text-muted)] mt-2 font-medium">Retrieving real-time signals from the ML pipeline.</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error || !caseData" class="flex flex-col items-center justify-center py-40 bg-[var(--surface-raised)] rounded-[3rem] border border-[var(--color-danger)]/20 shadow-2xl shadow-[var(--color-danger)]/5">
       <div class="w-20 h-20 bg-[var(--color-danger-muted)] rounded-[2rem] flex items-center justify-center mb-6 text-[var(--color-danger)] border border-[var(--color-danger)]/20">
          <AlertTriangle class="w-10 h-10" />
       </div>
       <h2 class="text-2xl font-black text-[var(--text-heading)] tracking-tight">Appraisal Document Not Found</h2>
       <p class="text-[var(--text-muted)] mt-2 font-medium">The requested case ID does not exist or has been archived.</p>
       <button @click="$router.back()" class="mt-8 px-8 py-3 bg-primary text-white text-xs font-black rounded-xl uppercase tracking-widest hover:scale-105 active:scale-95 transition-all">
          Return to Dashboard
       </button>
    </div>

    <!-- Main Content -->
    <template v-else>
      <!-- Case Header -->
      <header class="flex items-center justify-between bg-[var(--surface-raised)] border border-[var(--border-main)] p-10 rounded-[2rem] shadow-2xl relative overflow-hidden group">
        <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-primary via-[var(--color-info)] to-primary"></div>
        
        <div class="flex items-center gap-10">
          <ScoreGauge :score="caseData.score || 0" :size="140" />
          <div>
            <div class="flex items-center gap-4 mb-3">
              <h1 class="text-4xl font-black text-[var(--text-heading)] tracking-tight">{{ caseData.name }}</h1>
              <span 
                class="px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-widest flex items-center gap-1.5 border"
                :class="(caseData.score || 0) > 70 ? 'bg-[var(--color-success-muted)] text-[var(--color-success)] border-[var(--color-success)]/20' : 'bg-[var(--color-warning-muted)] text-[var(--color-warning)] border-[var(--color-warning)]/20'"
              >
                <CheckCircle v-if="(caseData.score || 0) > 70" class="w-3 h-3" />
                <AlertTriangle v-else class="w-3 h-3" />
                {{ (caseData.score || 0) > 70 ? 'Low Risk' : 'Medium Risk' }}
              </span>
            </div>
            <div class="grid grid-cols-2 gap-x-10 gap-y-2 text-xs text-[var(--text-label)] font-medium">
              <div class="flex items-center gap-2">
                <span class="font-black text-[var(--text-muted)] uppercase tracking-tighter">CIN</span>
                <span class="text-[var(--text-heading)] font-bold">{{ caseData.cin || 'N/A' }}</span>
              </div>
              <div class="flex items-center gap-2">
                <span class="font-black text-[var(--text-muted)] uppercase tracking-tighter">Sectors</span>
                <span class="text-[var(--text-heading)] font-bold">{{ caseData.sectors || 'General' }}</span>
              </div>
              <div class="flex items-center gap-2">
                <span class="font-black text-[var(--text-muted)] uppercase tracking-tighter">Established</span>
                <span class="text-[var(--text-heading)] font-bold">{{ caseData.established || 'N/A' }}</span>
              </div>
              <div class="flex items-center gap-2">
                <span class="font-black text-[var(--text-muted)] uppercase tracking-tighter">Rating</span>
                <span class="text-primary font-black">{{ caseData.rating || 'Unrated' }}</span>
              </div>
            </div>
          </div>
        </div>

        <div class="flex gap-4">
          <button @click="exportRawData" class="flex items-center gap-2 px-6 py-3 bg-[var(--surface-2)] hover:bg-[var(--surface-1)] text-[var(--text-heading)] text-sm font-black rounded-2xl transition-all active:scale-95 group border border-[var(--border-main)]">
            <Download class="w-4 h-4 text-[var(--text-muted)] group-hover:text-primary transition-colors" />
            Export Raw Data
          </button>
          <button @click="$router.push(`/case/${caseData.id}/cam`)" class="flex items-center gap-2 px-6 py-3 bg-primary hover:bg-primary-hover text-white text-sm font-black rounded-2xl transition-all shadow-xl shadow-primary/20 active:scale-95 group">
            <FileText class="w-4 h-4 transform group-hover:scale-110 transition-transform" />
            View CAM Document
          </button>
        </div>
      </header>

      <!-- Navigation Tabs -->
      <nav class="flex items-center p-2 bg-[var(--surface-raised)] border border-[var(--border-main)] rounded-2xl w-max ml-1 shadow-sm">
        <button 
          v-for="tab in [
            {id:'financials', icon: BarChart3},
            {id:'research', icon: Search},
            {id:'qualitative', icon: MessageSquare},
            {id:'scoring', icon: Gauge}
          ]" 
          :key="tab.id"
          @click="activeTab = tab.id"
          class="flex items-center gap-2 px-8 py-3 rounded-xl text-sm font-black capitalize transition-all active:scale-95"
          :class="activeTab === tab.id ? 'bg-[var(--color-selected-bg)] text-primary shadow-sm border border-primary/20' : 'text-[var(--text-muted)] hover:text-primary'"
        >
          <component :is="tab.icon" class="w-4 h-4" />
          {{ tab.id }}
        </button>
      </nav>

      <!-- Tab Content -->
      <div class="pt-2">
        <transition name="fade" mode="out-in">
          <div v-if="activeTab === 'financials'" key="financials" class="space-y-8">
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 px-1">
              <FinancialRatioCard v-for="ratio in ratios" :key="ratio.label" v-bind="ratio" />
            </div>
            <div class="bg-[var(--surface-raised)] border border-[var(--border-main)] p-12 rounded-[2.5rem] shadow-sm relative overflow-hidden">
              <header class="flex items-center justify-between mb-10">
                <div>
                  <h3 class="text-xl font-black text-[var(--text-heading)]">Historical Performance</h3>
                  <p class="text-sm text-[var(--text-muted)] mt-1 font-medium">Twelve month trailing revenue trend</p>
                </div>
                <div class="flex items-center gap-4">
                  <div class="flex items-center gap-2">
                    <div class="w-3 h-3 rounded-full bg-primary/20"></div>
                    <span class="text-[10px] font-black text-[var(--text-label)] uppercase tracking-[0.2em]">Revenue</span>
                  </div>
                </div>
              </header>
              <div class="h-64 flex items-end gap-3 px-4">
                <div v-for="i in 12" :key="i" class="flex-1 bg-primary/10 rounded-t-xl relative group transition-all hover:bg-primary/30 border-x border-t border-primary/5 hover:scale-x-105 origin-bottom" :style="{ height: (30 + (caseData.revenueTrend?.[i-1] || Math.random() * 70)) + '%' }">
                    <div class="absolute -top-12 left-1/2 -translate-x-1/2 bg-[var(--surface-raised)] border border-[var(--border-main)] text-[var(--text-heading)] text-[11px] font-black py-2 px-3 rounded-xl opacity-0 group-hover:opacity-100 transition-all pointer-events-none shadow-2xl transform translate-y-2 group-hover:translate-y-0 z-20">₹ {{ (caseData.revenueTrend?.[i-1] || Math.random()*100).toFixed(1)}} Cr</div>
                </div>
              </div>
              <div class="flex justify-between mt-8 px-4 text-[10px] font-black text-[var(--text-label)] uppercase tracking-[0.3em] opacity-60">
                <span>Apr 2025</span>
                <span>Mar 2026</span>
              </div>
            </div>

            <!-- Document Vault Section -->
            <div v-if="caseData.documents?.length" class="bg-[var(--surface-raised)] border border-[var(--border-main)] rounded-[3rem] p-12 shadow-sm relative overflow-hidden group">
              <div class="absolute -top-10 -right-10 w-40 h-40 bg-primary/5 blur-3xl"></div>
              <h3 class="text-xl font-black text-[var(--text-heading)] mb-10 flex items-center gap-4">
                <div class="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center text-primary border border-primary/20">
                  <FileText class="w-5 h-5" />
                </div>
                Source Document Vault
              </h3>
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <a 
                  v-for="doc in caseData.documents" 
                  :key="doc.url" 
                  :href="doc.url" 
                  target="_blank"
                  class="flex items-center gap-6 p-6 bg-[var(--surface-1)] rounded-[2rem] border border-[var(--border-main)] hover:border-primary/40 hover:bg-[var(--surface-raised)] hover:shadow-2xl transition-all group/doc"
                >
                  <div class="w-14 h-14 rounded-2xl flex items-center justify-center border transition-all group-hover/doc:scale-110 shadow-sm" 
                       :class="doc.type === 'application/pdf' ? 'bg-[var(--color-danger-muted)] border-[var(--color-danger)]/20 text-[var(--color-danger)]' : 'bg-[var(--color-success-muted)] border-[var(--color-success)]/20 text-[var(--color-success)]'">
                    <FileText v-if="doc.type === 'application/pdf'" class="w-7 h-7" />
                    <BarChart3 v-else class="w-7 h-7" />
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-black text-[var(--text-heading)] group-hover/doc:text-primary transition-colors truncate">{{ doc.name }}</p>
                    <p class="text-[10px] font-black text-[var(--text-muted)] mt-1 tracking-tighter uppercase opacity-60">{{ (doc.size / 1024 / 1024).toFixed(2) }} MB</p>
                  </div>
                  <Download class="w-4 h-4 text-[var(--text-muted)] opacity-0 group-hover/doc:opacity-100 transition-all transform translate-x-2 group-hover/doc:translate-x-0" />
                </a>
              </div>
            </div>
          </div>

          <div v-else-if="activeTab === 'research'" key="research" class="grid grid-cols-1 lg:grid-cols-3 gap-10">
            <div class="lg:col-span-2">
              <div class="bg-[var(--surface-raised)] border border-[var(--border-main)] rounded-[2.5rem] p-10 shadow-sm">
                <h3 class="text-xl font-black text-[var(--text-heading)] mb-10 flex items-center gap-4">
                  <div class="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center text-primary">
                    <Search class="w-5 h-5" />
                  </div>
                  Intelligence Feed
                </h3>
                <ResearchFeed :items="newsItems" />
                <div v-if="newsItems.length === 0" class="flex flex-col items-center justify-center py-20 opacity-30">
                   <div class="w-20 h-20 rounded-[2rem] bg-[var(--surface-1)] flex items-center justify-center mb-6">
                      <Search class="w-10 h-10" />
                   </div>
                   <p class="font-black uppercase tracking-widest text-xs">No research tokens detected</p>
                </div>
              </div>
            </div>
            <div class="space-y-8">
              <div class="bg-[var(--surface-raised)] border border-[var(--border-main)] rounded-[2.5rem] p-10 shadow-sm">
                <div class="flex items-center gap-3 mb-10">
                  <Activity class="w-4 h-4 text-primary" />
                  <h4 class="text-[10px] font-black text-[var(--text-label)] uppercase tracking-[0.2em]">Sentiment Analysis</h4>
                </div>
                <div class="flex items-center justify-between mb-6">
                    <div class="flex flex-col gap-1">
                      <div class="flex items-center gap-1.5">
                        <TrendingUp class="w-4 h-4 text-[var(--color-success)]" />
                        <span class="text-[var(--color-success)] text-sm font-black uppercase tracking-tighter">Positive</span>
                      </div>
                      <span class="text-2xl font-black text-[var(--text-heading)]">{{ caseData.sentiment?.positive || '0' }}%</span>
                    </div>
                    <div class="flex flex-col gap-1 text-right">
                      <div class="flex items-center gap-1.5 justify-end">
                        <TrendingDown class="w-4 h-4 text-[var(--color-danger)]" />
                        <span class="text-[var(--color-danger)] text-sm font-black uppercase tracking-tighter">Negative</span>
                      </div>
                      <span class="text-2xl font-black text-[var(--text-heading)]">{{ caseData.sentiment?.negative || '0' }}%</span>
                    </div>
                </div>
                <div class="h-4 w-full bg-[var(--surface-1)] rounded-full overflow-hidden flex shadow-inner">
                    <div class="h-full bg-[var(--color-success)] shadow-[0_0_10px_rgba(16,185,129,0.2)]" :style="{ width: (caseData.sentiment?.positive || 0) + '%' }"></div>
                    <div class="h-full bg-[var(--text-muted)]" :style="{ width: (caseData.sentiment?.neutral || 20) + '%' }"></div>
                    <div class="h-full bg-[var(--color-danger)]" :style="{ width: (caseData.sentiment?.negative || 0) + '%' }"></div>
                </div>
                <p class="mt-8 text-xs text-[var(--text-main)] font-medium leading-relaxed italic border-l-2 border-primary/20 pl-4">"{{ caseData.sentimentSummary || 'Market sentiment data being synthesized.' }}"</p>
              </div>
              
              <div class="bg-[var(--surface-raised)] border border-[var(--border-main)] rounded-[2.5rem] p-10 shadow-sm">
                <div class="flex items-center gap-3 mb-8">
                  <ShieldCheck class="w-4 h-4 text-primary" />
                  <h4 class="text-[10px] font-black text-[var(--text-label)] uppercase tracking-[0.2em]">Legal Watch</h4>
                </div>
                <div class="space-y-4">
                    <div class="flex items-center justify-between p-5 bg-[var(--surface-1)] rounded-2xl border border-[var(--border-main)] group hover:border-primary/30 transition-all">
                      <div class="text-[10px] font-black text-[var(--text-label)] uppercase tracking-widest">NCLT Actions</div>
                      <CheckCircle v-if="!caseData.legalFlags?.nclt" class="w-5 h-5 text-[var(--color-success)]" />
                      <AlertTriangle v-else class="w-5 h-5 text-[var(--color-danger)]" />
                    </div>
                    <div class="flex items-center justify-between p-5 bg-[var(--surface-1)] rounded-2xl border border-[var(--border-main)] group hover:border-primary/30 transition-all">
                      <div class="text-[10px] font-black text-[var(--text-label)] uppercase tracking-widest">Litigation</div>
                      <div v-if="caseData.legalFlags?.litigationCount" class="flex items-center gap-2 px-3 py-1.5 bg-[var(--color-warning-muted)] text-[var(--color-warning)] rounded-xl text-[10px] font-black border border-[var(--color-warning)]/20 shadow-sm transition-all group-hover:scale-105">
                        <AlertTriangle class="w-3 h-3" />
                        {{ caseData.legalFlags.litigationCount }} DETECTED
                      </div>
                      <CheckCircle v-else class="w-5 h-5 text-[var(--color-success)]" />
                    </div>
                </div>
              </div>
            </div>
          </div>

          <div v-else-if="activeTab === 'qualitative'" key="qualitative">
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-10">
              <div class="bg-[var(--surface-raised)] border border-[var(--border-main)] rounded-[2.5rem] p-12 shadow-sm">
                <h3 class="text-xl font-black text-[var(--text-heading)] mb-12 flex items-center gap-4">
                  <div class="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center text-primary">
                    <Quote class="w-5 h-5" />
                  </div>
                  Primary Due Diligence
                </h3>
                <div class="space-y-12">
                  <div v-for="q in (caseData.qualitative || [
                    {l:'Management Integrity', v:'High', d:'Promoters have strong market reputation and no history of defaults.'},
                    {l:'Operational Efficiency', v:'Good', d:'Plant utilization at 82% over the last two quarters.'},
                    {l:'Collateral Quality', v:'Standard', d:'Industrial land with residential conversion potential.'}
                  ])" :key="q.l" class="pb-10 border-b border-[var(--border-main)] last:border-0 last:pb-0 group">
                      <div class="flex items-center justify-between mb-4">
                        <div class="flex items-center gap-4">
                          <Activity class="w-5 h-5 text-[var(--text-muted)] group-hover:text-primary transition-colors" />
                          <span class="text-lg font-black text-[var(--text-heading)] tracking-tight">{{ q.l }}</span>
                        </div>
                        <span class="px-3 py-1 rounded-xl bg-[var(--color-selected-bg)] text-primary text-[10px] font-black uppercase border border-primary/20">{{ q.v }}</span>
                      </div>
                      <p class="text-sm text-[var(--text-main)] italic leading-relaxed pl-9 font-medium">"{{ q.d }}"</p>
                  </div>
                </div>
              </div>
              <div class="bg-[var(--color-info-muted)]/20 border border-[var(--color-info)]/10 rounded-[2.5rem] p-12 shadow-sm relative overflow-hidden">
                <div class="absolute -top-20 -right-20 w-64 h-64 bg-primary/5 blur-3xl"></div>
                <header class="mb-12 relative z-10">
                  <h3 class="text-xl font-black text-primary flex items-center gap-3">
                    <Sparkles class="w-6 h-6 animate-pulse" />
                    Recommended Adjustments
                  </h3>
                  <p class="text-sm text-[var(--text-main)] mt-2 font-medium">System-calculated override based on qualitative signals.</p>
                </header>
                <div class="space-y-6 relative z-10">
                    <div v-for="adj in (caseData.adjustments || [
                      {n:'Management Alpha', v:'+4', p:true, d:'Positive leading history'},
                      {n:'Sector Headwinds', v:'-2', p:false, d:'Material price volatility'}
                    ])" :key="adj.n" class="flex items-center justify-between p-8 bg-[var(--surface-raised)] rounded-[2.5rem] border border-[var(--border-main)] shadow-2xl shadow-primary/5 hover:-translate-y-1 transition-all group" :class="!adj.p && 'opacity-70 grayscale hover:grayscale-0 hover:opacity-100'">
                      <div class="flex flex-col gap-1">
                        <span class="text-[10px] font-black text-[var(--text-label)] uppercase tracking-[0.2em]">{{ adj.n }}</span>
                        <span class="text-sm font-black text-[var(--text-heading)]">{{ adj.d }}</span>
                      </div>
                      <div class="flex items-center gap-2 font-black px-3 py-2 rounded-2xl border border-opacity-10" :class="adj.p ? 'text-[var(--color-success)] bg-[var(--color-success-muted)] border-[var(--color-success)]' : 'text-[var(--color-danger)] bg-[var(--color-danger-muted)] border-[var(--color-danger)]'">
                        <TrendingUp v-if="adj.p" class="w-5 h-5" />
                        <TrendingDown v-else class="w-5 h-5" />
                        <span class="text-2xl tracking-tighter">{{ adj.v }}</span>
                      </div>
                    </div>
                </div>
                <div class="mt-14 p-8 bg-primary/10 rounded-3xl border border-primary/20 relative z-10">
                   <p class="text-xs text-primary leading-relaxed font-black">
                     <span class="italic opacity-70">EXECUTIVE NOTE:</span> {{ caseData.executiveNote || 'Adjustments reflect balanced risk-reward profile.' }}
                   </p>
                </div>
              </div>
            </div>
          </div>

          <div v-else-if="activeTab === 'scoring'" key="scoring" class="space-y-10">
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-10">
              <div class="bg-[var(--surface-raised)] border border-[var(--border-main)] rounded-[3rem] p-16 flex flex-col items-center relative overflow-hidden shadow-sm">
                <div class="absolute -top-10 -right-10 w-40 h-40 bg-[var(--color-success)]/5 blur-[60px]"></div>
                <h3 class="text-xl font-black text-[var(--text-heading)] mb-16 w-full flex items-center justify-between">
                    Scoring Recommendation
                    <div class="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center text-primary">
                      <Gauge class="w-5 h-5" />
                    </div>
                </h3>
                <ScoreGauge :score="caseData.score || 0" :size="280" />
                <div class="mt-16 text-center">
                    <div class="flex items-center gap-4 justify-center mb-4 transition-all hover:scale-105">
                      <div class="w-12 h-12 bg-[var(--color-success-muted)] rounded-2xl flex items-center justify-center border border-[var(--color-success)]/10 text-[var(--color-success)] shadow-lg shadow-[var(--color-success)]/10">
                        <CheckCircle class="w-7 h-7" />
                      </div>
                      <p class="text-6xl font-black text-[var(--color-success)] tracking-tighter uppercase">{{ caseData.decision || 'PENDING' }}</p>
                    </div>
                    <p class="text-sm text-[var(--text-main)] font-medium">Recommended Limit: <span class="text-[var(--text-heading)] font-black text-2xl tracking-tighter ml-2">₹ {{ caseData.limit || '0' }} Cr</span></p>
                </div>
              </div>
              <div class="bg-[var(--surface-raised)] border border-[var(--border-main)] rounded-[3rem] p-12 shadow-sm relative overflow-hidden">
                <div class="absolute -bottom-10 -left-10 w-40 h-40 bg-primary/5 blur-[60px]"></div>
                <h3 class="text-xl font-black text-[var(--text-heading)] mb-8 flex items-center gap-4">
                    <div class="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center text-primary">
                      <Zap class="w-5 h-5" />
                    </div>
                    Explainability Waterfall
                </h3>
                <p class="text-xs text-[var(--text-main)] mb-12 font-medium opacity-60">SHAP value contribution to final probability score.</p>
                <div class="space-y-8">
                    <div v-for="f in (caseData.waterfall || [
                      {n:'ICR', v:'+12.4', p:true},
                      {n:'Sector Index', v:'+8.1', p:true},
                      {n:'Sentiment', v:'+3.2', p:true},
                      {n:'D/E Ratio', v:'-2.5', p:false},
                      {n:'Litigations', v:'-5.8', p:false}
                    ])" :key="f.n" class="flex items-center gap-8 group">
                      <div class="w-44 flex items-center gap-4">
                          <div class="w-8 h-8 rounded-lg bg-[var(--surface-1)] flex items-center justify-center text-[var(--text-muted)] group-hover:text-primary transition-all border border-[var(--border-main)]">
                            <Activity class="w-4 h-4" />
                          </div>
                          <span class="text-[10px] font-black text-[var(--text-label)] group-hover:text-[var(--text-heading)] uppercase tracking-[0.2em] transition-colors leading-none">{{ f.n }}</span>
                      </div>
                      <div class="flex-1 h-2 bg-[var(--surface-2)] rounded-full overflow-hidden relative shadow-inner">
                          <div 
                            class="absolute h-full rounded-full transition-all duration-1000" 
                            :class="f.p ? 'bg-[var(--color-success)] right-1/2 shadow-[0_0_10px_rgba(16,185,129,0.3)]' : 'bg-[var(--color-danger)] left-1/2 shadow-[0_0_10px_rgba(239,68,68,0.3)]'"
                            :style="{ width: (Math.abs(parseFloat(f.v)) * 4) + '%'}"
                          ></div>
                      </div>
                      <span class="w-20 text-sm font-black text-right transition-all group-hover:scale-110" :class="f.p ? 'text-[var(--color-success)]' : 'text-[var(--color-danger)]'">{{ f.v }}</span>
                    </div>
                </div>
                <div class="mt-16 p-10 bg-[var(--surface-1)] rounded-[2.5rem] border border-[var(--border-main)] relative shadow-inner group hover:border-primary/20 transition-all">
                    <Quote class="w-10 h-10 text-primary/10 absolute top-6 left-6 group-hover:scale-125 transition-transform" />
                    <p class="text-sm text-[var(--text-main)] leading-relaxed relative z-10 font-medium pl-4 border-l-2 border-primary/20">
                      <span class="font-black text-primary uppercase tracking-widest text-[10px] block mb-2">Decision Rationale:</span> {{ caseData.rationale || 'The system found sufficient solvency indicators to support a positive recommendation.' }}
                    </p>
                </div>
              </div>
            </div>
          </div>
        </transition>
      </div>
    </template>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(15px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(-15px);
}
</style>
