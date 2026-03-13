<template>
  <div class="bg-[var(--surface-raised)] p-12 rounded-[3rem] border border-[var(--border-main)] shadow-sm relative overflow-hidden group">
    <div class="absolute -top-10 -right-10 w-40 h-40 bg-primary/5 blur-3xl group-hover:bg-primary/10 transition-colors"></div>
    
    <div class="flex items-center gap-5 mb-10 relative z-10">
      <div class="w-14 h-14 rounded-2xl bg-primary/10 text-primary flex items-center justify-center border border-primary/20 shadow-lg shadow-primary/5 group-hover:scale-110 transition-transform duration-500">
        <MessageSquare class="w-7 h-7" />
      </div>
      <h2 class="text-3xl font-black text-[var(--text-heading)] tracking-tighter">Qualitative Observations</h2>
    </div>
    
    <div class="p-12 bg-[var(--surface-1)] rounded-[2.5rem] border border-dashed border-[var(--border-main)] flex flex-col items-center justify-center text-center gap-6 relative z-10 group-hover:border-primary/30 transition-colors">
      <div class="w-20 h-20 rounded-[1.5rem] bg-[var(--surface-raised)] flex items-center justify-center border border-[var(--border-main)] shadow-inner transform group-hover:rotate-12 transition-transform duration-500">
        <Sparkles class="w-10 h-10 text-primary opacity-30 animate-pulse" />
      </div>
      <div class="max-w-md">
        <p class="text-[var(--text-main)] font-black text-lg italic opacity-40 leading-relaxed">
          "Form for primary due diligence findings is being synthesized by AI. Please check back shortly."
        </p>
      </div>
      <div class="flex gap-2">
        <div v-for="i in 3" :key="i" class="w-2 h-2 rounded-full bg-primary/20 animate-bounce" :style="{ animationDelay: (i * 0.2) + 's' }"></div>
      </div>
    </div>
  </div>
</template>
