<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  score: number
  size?: number
}>()

const radius = 90
const circumference = 2 * Math.PI * radius
const strokeDashoffset = computed(() => circumference - (props.score / 100) * circumference)

const colorClass = computed(() => {
  if (props.score >= 80) return 'text-emerald-500'
  if (props.score >= 60) return 'text-blue-500'
  if (props.score >= 40) return 'text-amber-500'
  return 'text-red-500'
})

const shadowClass = computed(() => {
  if (props.score >= 80) return 'drop-shadow-[0_0_15px_rgba(16,185,129,0.3)]'
  if (props.score >= 60) return 'drop-shadow-[0_0_15px_rgba(59,130,246,0.3)]'
  if (props.score >= 40) return 'drop-shadow-[0_0_15px_rgba(245,158,11,0.3)]'
  return 'drop-shadow-[0_0_15px_rgba(239,68,68,0.3)]'
})
</script>

<template>
  <div class="relative flex items-center justify-center" :style="{ width: size ? size + 'px' : '240px', height: size ? size + 'px' : '240px' }">
    <svg class="transform -rotate-90 w-full h-full" viewBox="0 0 200 200">
      <!-- Background Circle -->
      <circle
        cx="100"
        cy="100"
        :r="radius"
        stroke="currentColor"
        stroke-width="12"
        fill="transparent"
        class="text-slate-800"
      />
      <!-- Progress Circle -->
      <circle
        cx="100"
        cy="100"
        :r="radius"
        stroke="currentColor"
        stroke-width="12"
        fill="transparent"
        :stroke-dasharray="circumference"
        :style="{ strokeDashoffset: strokeDashoffset }"
        stroke-linecap="round"
        class="transition-all duration-1000 ease-out"
        :class="[colorClass, shadowClass]"
      />
    </svg>
    <div class="absolute inset-0 flex flex-col items-center justify-center">
      <span class="text-5xl font-black tracking-tighter" :class="colorClass">
        {{ Math.round(score) }}
      </span>
      <span class="text-xs font-bold text-slate-500 uppercase tracking-widest mt-1">Credit Score</span>
    </div>
  </div>
</template>
