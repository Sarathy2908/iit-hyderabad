<script setup lang="ts">
import { 
  ExternalLink, 
  AlertTriangle, 
  Newspaper, 
  CheckCircle,
  Clock
} from 'lucide-vue-next'

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

const sentimentConfig = {
  positive: { color: 'text-[var(--color-success)] bg-[var(--color-success-muted)] border-[var(--color-success)]/20', icon: CheckCircle },
  negative: { color: 'text-[var(--color-danger)] bg-[var(--color-danger-muted)] border-[var(--color-danger)]/20', icon: AlertTriangle },
  neutral: { color: 'text-[var(--text-label)] bg-[var(--surface-2)] border-[var(--border-main)]', icon: Newspaper },
  risk: { color: 'text-[var(--color-warning)] bg-[var(--color-warning-muted)] border-[var(--color-warning)]/20', icon: AlertTriangle }
}
</script>

<template>
  <div class="space-y-4">
    <div v-for="item in items" :key="item.id" class="p-6 bg-[var(--surface-1)] border border-[var(--border-main)] rounded-2xl hover:border-primary/40 hover:bg-[var(--surface-raised)] transition-all group shadow-sm">
      <div class="flex items-start justify-between gap-6">
        <div class="flex-1">
          <div class="flex items-center gap-4 mb-4">
            <div :class="['px-3 py-1 rounded-lg text-[10px] font-black uppercase border flex items-center gap-2 transition-all shadow-sm', sentimentConfig[item.sentiment].color]">
              <component :is="sentimentConfig[item.sentiment].icon" class="w-3.5 h-3.5" />
              {{ item.sentiment }}
            </div>
            <div class="flex items-center gap-2 text-[11px] font-black text-[var(--text-muted)] tracking-tight">
              <span class="text-[var(--text-heading)] underline decoration-primary/20">{{ item.source }}</span>
              <span class="opacity-20">/</span>
              <div class="flex items-center gap-1.5 px-2 py-0.5 bg-[var(--surface-2)] rounded-md border border-[var(--border-main)]/50">
                <Clock class="w-3 h-3" />
                {{ item.date }}
              </div>
            </div>
          </div>
          <h4 class="text-base font-black text-[var(--text-heading)] group-hover:text-primary transition-colors leading-relaxed tracking-tight">
            {{ item.title }}
          </h4>
          <p v-if="item.summary" class="text-xs text-[var(--text-main)] mt-3 leading-relaxed font-medium line-clamp-2 pl-0.5 border-l-2 border-[var(--border-main)] pl-4">
            {{ item.summary }}
          </p>
        </div>
        <button class="p-3 text-[var(--text-muted)] hover:text-primary bg-[var(--surface-2)] hover:bg-primary/10 border border-[var(--border-main)] rounded-xl transition-all active:scale-90 shadow-sm">
          <ExternalLink class="w-4 h-4" />
        </button>
      </div>
    </div>
  </div>
</template>
