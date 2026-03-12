<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  label: string
  value: string | number
  trend?: 'up' | 'down' | 'stable'
  unit?: string
  description?: string
}>()

const trendColor = computed(() => {
  if (props.trend === 'up') return 'text-emerald-400 bg-emerald-400/10'
  if (props.trend === 'down') return 'text-red-400 bg-red-400/10'
  return 'text-slate-400 bg-slate-400/10'
})
</script>

<template>
  <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl hover:border-slate-700 transition-all group">
    <div class="flex items-center justify-between mb-3">
      <span class="text-xs font-bold text-slate-500 uppercase tracking-wider">{{ label }}</span>
      <div v-if="trend" :class="['px-2 py-0.5 rounded-full text-[10px] font-bold uppercase', trendColor]">
        {{ trend }}
      </div>
    </div>
    <div class="flex items-baseline space-x-1">
      <span class="text-3xl font-bold text-slate-100 group-hover:text-blue-400 transition-colors">{{ value }}</span>
      <span v-if="unit" class="text-sm font-medium text-slate-500">{{ unit }}</span>
    </div>
    <p v-if="description" class="text-xs text-slate-400 mt-2 leading-relaxed">{{ description }}</p>
  </div>
</template>
