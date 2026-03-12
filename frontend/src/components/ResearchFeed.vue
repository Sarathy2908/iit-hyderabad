<script setup lang="ts">
interface NewsItem {
  id: string
  title: string
  source: string
  date: string
  sentiment: 'positive' | 'negative' | 'neutral' | 'risk'
  summary?: string
}

defineProps<{
  items: NewsItem[]
}>()

const sentimentClasses = {
  positive: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
  negative: 'bg-red-500/10 text-red-400 border-red-500/20',
  neutral: 'bg-slate-500/10 text-slate-400 border-slate-500/20',
  risk: 'bg-amber-500/10 text-amber-400 border-amber-500/20'
}
</script>

<template>
  <div class="space-y-4">
    <div v-for="item in items" :key="item.id" class="p-4 bg-slate-900 border border-slate-800 rounded-xl hover:border-slate-700 transition-colors group">
      <div class="flex items-start justify-between gap-4">
        <div class="flex-1">
          <div class="flex items-center space-x-2 mb-2">
            <span :class="['px-2 py-0.5 rounded-full text-[10px] font-bold uppercase border', sentimentClasses[item.sentiment]]">
              {{ item.sentiment }}
            </span>
            <span class="text-[11px] font-medium text-slate-500">{{ item.source }} • {{ item.date }}</span>
          </div>
          <h4 class="text-sm font-semibold text-slate-200 group-hover:text-blue-400 transition-colors leading-snug">
            {{ item.title }}
          </h4>
          <p v-if="item.summary" class="text-xs text-slate-400 mt-2 line-clamp-2">{{ item.summary }}</p>
        </div>
        <button class="p-2 text-slate-600 hover:text-slate-400 transition-colors">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
        </button>
      </div>
    </div>
  </div>
</template>
