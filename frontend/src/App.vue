<script setup lang="ts">
import { RouterView } from 'vue-router'
</script>

<template>
  <div class="min-h-screen w-full bg-slate-950 text-slate-100 font-sans selection:bg-blue-500/30">
    <!-- Premium Navigation -->
    <nav class="sticky top-0 z-50 bg-slate-900/80 backdrop-blur-md border-b border-slate-800">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <span class="text-2xl font-black bg-gradient-to-r from-blue-400 to-indigo-500 bg-clip-text text-transparent">
                INTELLI-CREDIT
              </span>
            </div>
            <div class="hidden md:block ml-10">
              <div class="flex items-baseline space-x-4">
                <router-link to="/" class="text-slate-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors">Dashboard</router-link>
                <router-link to="/case/new" class="text-slate-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors">New Case</router-link>
                <router-link to="/admin" class="text-slate-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors">Admin</router-link>
              </div>
            </div>
          </div>
          <div class="flex items-center">
            <div class="bg-slate-800 h-8 w-8 rounded-full flex items-center justify-center border border-slate-700">
              <span class="text-xs font-bold text-blue-400">CU</span>
            </div>
            <span class="ml-2 text-sm font-medium text-slate-400">Credit User</span>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <transition 
        name="fade" 
        mode="out-in"
      >
        <RouterView />
      </transition>
    </main>

    <!-- Visual Accents -->
    <div class="fixed top-0 right-0 -z-10 h-[500px] w-[500px] rounded-full bg-blue-500/10 blur-[120px]"></div>
    <div class="fixed bottom-0 left-0 -z-10 h-[500px] w-[500px] rounded-full bg-indigo-500/10 blur-[120px]"></div>
  </div>
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.router-link-active {
  @apply text-blue-400 bg-slate-800/50;
}
</style>
