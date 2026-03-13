<script setup lang="ts">
import { ref, computed } from 'vue'
import { 
  Settings, 
  BarChart3, 
  Activity, 
  Radio, 
  ShieldCheck, 
  Zap, 
  Save, 
  ShieldAlert, 
  MoreVertical,
  Loader2
} from 'lucide-vue-next'
import { useDocument } from 'vuefire'
import { doc, setDoc } from 'firebase/firestore'
import { db } from '../firebase'

// Global system settings from Firestore
const settingsRef = doc(db, 'settings', 'global')
const { data: systemSettings, pending } = useDocument(settingsRef)

const isSaving = ref(false)

// Default fallbacks while data loads or if missing
const weights = computed(() => systemSettings.value?.weights || [
  { l: 'Financial Ratios (Capacity)', v: 40, i: 'Activity' },
  { l: 'News Sentiment (Character)', v: 25, i: 'Radio' },
  { l: 'Historical Repayment', v: 20, i: 'ShieldCheck' },
  { l: 'Qualitative Overrides', v: 15, i: 'Zap' }
])

const benchmarks = computed(() => systemSettings.value?.benchmarks || [
  { s: 'Steel', a: '1.25x', r: 'Low', c: 'text-[var(--color-success)]', bg: 'bg-[var(--color-success-muted)]', b: 'border-[var(--color-success)]/20' },
  { s: 'Infrastructure', a: '1.1x', r: 'Moderate', c: 'text-[var(--color-warning)]', bg: 'bg-[var(--color-warning-muted)]', b: 'border-[var(--color-warning)]/20' },
  { s: 'Real Estate', a: '0.85x', r: 'High', c: 'text-[var(--color-danger)]', bg: 'bg-[var(--color-danger-muted)]', b: 'border-[var(--color-danger)]/20' },
  { s: 'IT / SaaS', a: '2.4x', r: 'Minimal', c: 'text-primary', bg: 'bg-[var(--color-selected-bg)]', b: 'border-primary/20' }
])

const thresholds = computed(() => systemSettings.value?.thresholds || [
  { t: 'GST Variance', v: '> 15%', d: 'Flag gap between 2A and 3B.', c: 'text-[var(--color-danger)]' },
  { t: 'News Multiplier', v: '3x', d: 'Weight for negative regulatory news.', c: 'text-primary' },
  { t: 'Cheque Bounce', v: '2/qr', d: 'Max frequency before downgrade.', c: 'text-[var(--color-warning)]' }
])

async function handleSave() {
  isSaving.value = true
  try {
    // In a real app, we'd have inputs to modify these. 
    // For now, we ensure they are persisted if they were changed locally.
    await setDoc(settingsRef, {
      weights: weights.value,
      benchmarks: benchmarks.value,
      thresholds: thresholds.value,
      lastUpdated: new Date().toISOString()
    }, { merge: true })
  } catch (err) {
    console.error("Failed to save settings:", err)
    alert("Error saving configuration.")
  } finally {
    isSaving.value = false
  }
}

// Icon mapper for component resolution
const iconMap:Record<string, any> = { Activity, Radio, ShieldCheck, Zap }
</script>

<template>
  <div class="max-w-7xl mx-auto pb-20 space-y-16">
    <header class="flex items-center gap-6 px-2">
      <div class="w-16 h-16 rounded-[2rem] bg-primary/10 text-primary flex items-center justify-center border-2 border-primary/20 shadow-xl shadow-primary/5">
        <Settings class="w-10 h-10" />
      </div>
      <div>
        <h1 class="text-5xl font-black text-[var(--text-heading)] tracking-tighter">System Configuration</h1>
        <p class="text-[var(--text-main)] mt-2 font-black italic opacity-60 flex items-center gap-2">
          <div class="w-1.5 h-1.5 rounded-full bg-primary/40"></div>
          Manage scoring weights, sector benchmarks, and risk thresholds.
        </p>
      </div>
    </header>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-16">
      <!-- Scoring Weights -->
      <section class="bg-[var(--surface-raised)] border border-[var(--border-main)] rounded-[3rem] p-12 shadow-sm relative overflow-hidden group">
        <div class="absolute -top-20 -right-20 w-64 h-64 bg-primary/5 blur-3xl group-hover:bg-primary/10 transition-colors"></div>
        <h2 class="text-2xl font-black text-[var(--text-heading)] mb-12 flex items-center justify-between relative z-10">
          <div class="flex items-center gap-4">
             <div class="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center text-primary border border-primary/20">
               <BarChart3 class="w-5 h-5" />
             </div>
             Scoring Engine Calibration
          </div>
          <span class="text-[10px] font-black text-primary uppercase tracking-[0.2em] bg-[var(--color-selected-bg)] border border-primary/20 px-4 py-1.5 rounded-full shadow-sm">Total: 100%</span>
        </h2>
        
        <div v-if="pending" class="py-20 flex flex-col items-center justify-center space-y-4 opacity-30">
           <Loader2 class="w-10 h-10 animate-spin" />
           <p class="text-[10px] font-black uppercase tracking-widest">Loading model weights...</p>
        </div>
        
        <div v-else class="space-y-12 relative z-10">
          <div v-for="w in weights" :key="w.l" class="space-y-5">
             <div class="flex justify-between items-end px-1">
                <div class="flex items-center gap-4">
                   <div class="w-8 h-8 rounded-lg bg-[var(--surface-1)] flex items-center justify-center text-[var(--text-muted)] border border-[var(--border-main)]">
                     <component :is="iconMap[w.i]" class="w-4 h-4" />
                   </div>
                   <span class="text-[10px] font-black text-[var(--text-label)] uppercase tracking-[0.2em] leading-none">{{ w.l }}</span>
                </div>
                <span class="text-2xl font-black text-primary tracking-tighter">{{ w.v }}%</span>
             </div>
             <div class="h-4 w-full bg-[var(--surface-1)] rounded-full overflow-hidden shadow-inner p-1">
                <div class="h-full bg-primary rounded-full shadow-[0_0_10px_rgba(var(--primary),0.3)] transition-all duration-1000 origin-left" :style="{ width: w.v + '%' }"></div>
             </div>
          </div>
        </div>

        <button 
          @click="handleSave"
          :disabled="isSaving"
          class="w-full mt-14 py-6 bg-primary hover:bg-primary-hover text-white font-black rounded-[2rem] transition-all shadow-2xl shadow-primary/20 active:scale-95 flex items-center justify-center gap-4 uppercase tracking-[0.3em] text-xs disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <Loader2 v-if="isSaving" class="w-6 h-6 animate-spin" />
          <Save v-else class="w-6 h-6" />
          {{ isSaving ? 'Syncing with Firestore...' : 'Update Model Weights' }}
        </button>
      </section>

      <!-- Sector Benchmarks -->
      <section class="bg-[var(--surface-raised)] border border-[var(--border-main)] rounded-[3rem] p-12 shadow-sm relative overflow-hidden">
        <h2 class="text-2xl font-black text-[var(--text-heading)] mb-12 flex items-center gap-4">
          <div class="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center text-primary border border-primary/20">
            <ShieldAlert class="w-5 h-5" />
          </div>
          Sector Risk Benchmarks
        </h2>
        
        <div v-if="pending" class="py-20 flex flex-col items-center justify-center space-y-4 opacity-30">
           <Loader2 class="w-10 h-10 animate-spin" />
           <p class="text-[10px] font-black uppercase tracking-widest">Syncing benchmarks...</p>
        </div>

        <div v-else class="overflow-x-auto">
           <table class="w-full text-left">
             <thead class="text-[10px] font-black text-[var(--text-label)] uppercase tracking-[0.2em] border-b border-[var(--border-main)]">
               <tr>
                 <th class="py-6 pl-2">Sector</th>
                 <th class="py-6">Avg. DSCR</th>
                 <th class="py-6">Risk Level</th>
                 <th class="py-6 text-right pr-2">Actions</th>
               </tr>
             </thead>
             <tbody class="text-sm text-[var(--text-main)]">
               <tr v-for="row in benchmarks" :key="row.s" class="border-b border-[var(--border-main)]/50 hover:bg-[var(--surface-1)] transition-all group">
                 <td class="py-6 font-black pl-2 tracking-tight text-[var(--text-heading)]">{{ row.s }}</td>
                 <td class="py-6 font-black text-[var(--text-muted)] tracking-tighter">{{ row.a }}</td>
                 <td class="py-6">
                    <span :class="[row.c, row.bg, row.b, 'px-3 py-1.5 rounded-xl border font-black text-[9px] uppercase tracking-widest shadow-sm inline-flex items-center']">
                      {{ row.r }}
                    </span>
                 </td>
                 <td class="py-6 text-right pr-2">
                    <button class="p-3 text-[var(--text-muted)] hover:text-primary bg-[var(--surface-1)] rounded-2xl border border-[var(--border-main)]/50 transition-all active:scale-75 shadow-sm">
                       <MoreVertical class="w-5 h-5" />
                    </button>
                 </td>
               </tr>
             </tbody>
           </table>
        </div>
      </section>
    </div>

    <!-- Alert Thresholds -->
    <div class="bg-[var(--surface-raised)] border border-[var(--border-main)] rounded-[3rem] p-12 shadow-sm relative overflow-hidden">
       <div class="absolute -bottom-20 -left-20 w-80 h-80 bg-primary/5 blur-[100px]"></div>
       <h2 class="text-2xl font-black text-[var(--text-heading)] mb-12 flex items-center gap-4">
         <div class="w-10 h-10 rounded-xl bg-[var(--color-warning-muted)] flex items-center justify-center text-[var(--color-warning)] border border-[var(--color-warning)]/20">
           <Radio class="w-6 h-6 animate-pulse" />
         </div>
         Real-time Warning Thresholds
       </h2>
       
       <div v-if="pending" class="py-20 flex flex-col items-center justify-center space-y-4 opacity-30">
           <Loader2 class="w-10 h-10 animate-spin" />
           <p class="text-[10px] font-black uppercase tracking-widest">Initializing monitors...</p>
       </div>

       <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-10 relative z-10">
          <div v-for="t in thresholds" :key="t.t" class="p-10 bg-[var(--surface-1)] rounded-[2.5rem] border border-[var(--border-main)] hover:border-primary/40 hover:bg-[var(--surface-raised)] transition-all group shadow-sm hover:shadow-2xl">
             <div class="flex items-center justify-between mb-8">
                <span class="text-[10px] font-black text-[var(--text-label)] uppercase tracking-[0.2em] opacity-60">{{ t.t }}</span>
                <span class="text-2xl font-black tracking-tighter px-4 py-1.5 rounded-2xl border border-[var(--border-main)] bg-[var(--surface-raised)] shadow-inner transition-all group-hover:scale-110" :class="t.c">{{ t.v }}</span>
             </div>
             <div class="pl-4 border-l-2 border-primary/20">
               <p class="text-[13px] text-[var(--text-main)] leading-relaxed font-black opacity-80 group-hover:opacity-100 transition-opacity">"{{ t.d }}"</p>
             </div>
          </div>
       </div>
    </div>
  </div>
</template>
