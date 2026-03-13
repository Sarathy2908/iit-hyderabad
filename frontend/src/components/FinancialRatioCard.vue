<script setup lang="ts">
import { computed } from 'vue'
import { 
  TrendingUp, 
  TrendingDown, 
  Minus 
} from 'lucide-vue-next'

const props = defineProps<{
  label: string
  value: string | number
  trend?: 'up' | 'down' | 'stable'
  unit?: string
  description?: string
}>()

const trendConfig = computed(() => {
  if (props.trend === 'up') return { color: 'text-[var(--color-success)] bg-[var(--color-success-muted)] border-[var(--color-success)]/20', icon: TrendingUp }
  if (props.trend === 'down') return { color: 'text-[var(--color-danger)] bg-[var(--color-danger-muted)] border-[var(--color-danger)]/20', icon: TrendingDown }
  return { color: 'text-[var(--text-label)] bg-[var(--surface-2)] border-[var(--border-main)]', icon: Minus }
})
</script>

<template>
  <div class="bg-[var(--surface-raised)] border border-[var(--border-main)] p-8 rounded-[2.5rem] hover:border-primary/40 transition-all group shadow-sm hover:shadow-2xl hover:-translate-y-1">
    <div class="flex items-center justify-between mb-6">
      <span class="text-[10px] font-black text-[var(--text-label)] uppercase tracking-[0.2em] leading-none">{{ label }}</span>
      <div v-if="trend" :class="['px-3 py-1.5 rounded-xl text-[10px] font-black uppercase flex items-center gap-1.5 border shadow-sm transition-all group-hover:scale-105', trendConfig.color]">
        <component :is="trendConfig.icon" class="w-3.5 h-3.5" />
        {{ trend }}
      </div>
    </div>
    <div class="flex items-baseline space-x-2">
      <span class="text-4xl font-black text-[var(--text-heading)] group-hover:text-primary transition-colors tracking-tighter">{{ value }}</span>
      <span v-if="unit" class="text-base font-black text-[var(--text-muted)] tracking-tighter">{{ unit }}</span>
    </div>
    <div v-if="description" class="mt-6 pt-4 border-t border-[var(--border-main)]/50">
      <p class="text-[11px] text-[var(--text-main)] leading-relaxed font-medium pl-0.5 opacity-80 italic">"{{ description }}"</p>
    </div>
  </div>
</template>
