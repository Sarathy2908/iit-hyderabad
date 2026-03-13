<script setup lang="ts">
import { ref } from 'vue'
import { RouterView, RouterLink } from 'vue-router'
import { useThemeStore } from './stores/theme'
import { 
  LayoutDashboard, 
  PlusCircle, 
  Settings, 
  Sun, 
  Moon,
  User,
  Zap
} from 'lucide-vue-next'

const themeStore = useThemeStore()

const userProfile = ref({
  role: 'Credit Manager',
  title: 'Senior Analyst'
})
</script>

<template>
  <div class="min-h-screen w-full bg-[var(--bg-app)] text-[var(--text-main)] font-sans selection:bg-primary/20 transition-colors duration-500 overflow-x-hidden">
    <!-- Premium Navigation -->
    <nav class="sticky top-0 z-50 bg-[var(--surface-raised)]/90 backdrop-blur-xl border-b border-[var(--border-main)] shadow-sm">
      <div class="max-w-[1920px] mx-auto px-6 sm:px-10 lg:px-16">
        <div class="flex items-center justify-between h-20">
          <div class="flex items-center gap-12">
            <div class="flex-shrink-0 flex items-center gap-3 group cursor-pointer">
              <div class="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center border border-primary/20 shadow-lg shadow-primary/5 group-hover:scale-110 group-hover:rotate-6 transition-all duration-500">
                <Zap class="w-6 h-6 text-primary fill-primary/20" />
              </div>
              <span class="text-2xl font-black bg-gradient-to-r from-primary via-[var(--color-info)] to-primary bg-clip-text text-transparent tracking-tighter bg-[length:200%_auto] animate-gradient">
                INTELLI-CREDIT
              </span>
            </div>
            <div class="hidden md:block">
              <div class="flex items-center space-x-2">
                <RouterLink to="/" class="nav-link">
                  <LayoutDashboard class="w-4 h-4" />
                  Dashboard
                </RouterLink>
                <RouterLink to="/case/new" class="nav-link">
                  <PlusCircle class="w-4 h-4" />
                  New Case
                </RouterLink>
                <RouterLink to="/admin" class="nav-link">
                  <Settings class="w-4 h-4" />
                  Admin
                </RouterLink>
              </div>
            </div>
          </div>
          <div class="flex items-center gap-8">
            <!-- Theme Toggle -->
            <button 
              @click="themeStore.toggleTheme" 
              class="p-3 rounded-2xl bg-[var(--surface-1)] hover:bg-[var(--surface-2)] text-[var(--text-muted)] hover:text-[var(--text-heading)] transition-all active:scale-95 border border-[var(--border-main)]/50 shadow-inner group"
              title="Toggle Theme"
            >
              <Sun v-if="themeStore.theme === 'dark'" class="w-5 h-5 group-hover:rotate-90 transition-transform duration-500" />
              <Moon v-else class="w-5 h-5 group-hover:-rotate-12 transition-transform duration-500" />
            </button>

            <div class="flex items-center gap-5 pl-8 border-l border-[var(--border-main)]">
              <div class="flex flex-col items-end hidden sm:block">
                <p class="text-[11px] font-black text-[var(--text-heading)] uppercase tracking-[0.2em] leading-none mb-1">{{ userProfile.role }}</p>
                <p class="text-[9px] font-black text-[var(--text-muted)] uppercase tracking-widest opacity-60">{{ userProfile.title }}</p>
              </div>
              <div class="bg-[var(--surface-raised)] h-12 w-12 rounded-2xl flex items-center justify-center border-2 border-primary/20 shadow-xl shadow-primary/5 relative group cursor-pointer hover:border-primary/40 transition-all">
                <User class="w-6 h-6 text-primary" />
                <div class="absolute -top-1 -right-1 w-3.5 h-3.5 bg-[var(--color-success)] border-2 border-[var(--surface-raised)] rounded-full shadow-sm"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="max-w-[1920px] mx-auto py-12 px-6 sm:px-10 lg:px-16">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- Global Background Elements -->
    <div class="fixed top-0 right-0 -z-10 h-[800px] w-[800px] rounded-full bg-primary/5 blur-[150px] pointer-events-none opacity-50"></div>
    <div class="fixed bottom-0 left-0 -z-10 h-[800px] w-[800px] rounded-full bg-[var(--color-info)]/5 blur-[150px] pointer-events-none opacity-50"></div>
  </div>
</template>

<style>
@reference "./style.css";

@keyframes gradient {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.animate-gradient {
  animation: gradient 5s ease infinite;
}

.nav-link {
  @apply flex items-center gap-3 px-6 py-2.5 rounded-2xl text-[11px] font-black uppercase tracking-[0.2em] text-[var(--text-muted)] hover:text-[var(--text-heading)] hover:bg-[var(--surface-1)] transition-all border border-transparent;
}

.router-link-active.nav-link {
  @apply text-primary bg-[var(--color-selected-bg)] border-primary/20 shadow-sm shadow-primary/5;
}

.fade-enter-active,
.fade-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(12px) scale(0.99);
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(-12px) scale(1.01);
}

::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: var(--bg-app);
}

::-webkit-scrollbar-thumb {
  background: var(--surface-2);
  border-radius: 10px;
  border: 2px solid var(--bg-app);
}

::-webkit-scrollbar-thumb:hover {
  background: var(--border-main);
}
</style>
