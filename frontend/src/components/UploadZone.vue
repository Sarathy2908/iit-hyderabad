<script setup lang="ts">
import { ref } from 'vue'

const isDragging = ref(false)
const files = ref<File[]>([])

const onDragOver = (e: DragEvent) => {
  e.preventDefault()
  isDragging.value = true
}

const onDragLeave = () => {
  isDragging.value = false
}

const onDrop = (e: DragEvent) => {
  e.preventDefault()
  isDragging.value = false
  if (e.dataTransfer?.files) {
    addFiles(Array.from(e.dataTransfer.files))
  }
}

const onFileSelect = (e: Event) => {
  const target = e.target as HTMLInputElement
  if (target.files) {
    addFiles(Array.from(target.files))
  }
}

const addFiles = (newFiles: File[]) => {
  files.value = [...files.value, ...newFiles]
}

const removeFile = (index: number) => {
  files.value.splice(index, 1)
}
</script>

<template>
  <div class="w-full">
    <div
      class="border-2 border-dashed rounded-2xl p-10 text-center transition-all duration-300"
      :class="isDragging ? 'border-blue-500 bg-blue-500/10' : 'border-slate-700 bg-slate-900/50 hover:border-slate-600'"
      @dragover="onDragOver"
      @dragleave="onDragLeave"
      @drop="onDrop"
    >
      <input
        type="file"
        multiple
        class="hidden"
        id="fileInput"
        @change="onFileSelect"
      />
      <label for="fileInput" class="cursor-pointer">
        <div class="flex flex-col items-center">
          <div class="w-16 h-16 bg-blue-500/20 rounded-full flex items-center justify-center mb-4">
            <svg class="w-8 h-8 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
          </div>
          <h3 class="text-xl font-semibold text-slate-100">Upload Financial Documents</h3>
          <p class="text-slate-400 mt-2">PDF, CSV, or XML files. Max 50MB per file.</p>
          <div class="mt-6 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-white font-medium transition-colors">
            Browse Files
          </div>
        </div>
      </label>
    </div>

    <!-- File List -->
    <div v-if="files.length > 0" class="mt-8 space-y-3">
      <h4 class="text-sm font-semibold text-slate-400 uppercase tracking-wider">Selected Files</h4>
      <div v-for="(file, index) in files" :key="index" class="flex items-center justify-between p-4 bg-slate-800/50 rounded-xl border border-slate-700/50">
        <div class="flex items-center space-x-4">
          <div class="p-2 bg-slate-700 rounded-lg">
            <svg v-if="file.type === 'application/pdf'" class="w-6 h-6 text-red-400" fill="currentColor" viewBox="0 0 20 20"><path d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z"/></svg>
            <svg v-else class="w-6 h-6 text-green-400" fill="currentColor" viewBox="0 0 20 20"><path d="M3 10a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z"/></svg>
          </div>
          <div>
            <p class="text-sm font-medium text-slate-200">{{ file.name }}</p>
            <p class="text-xs text-slate-500">{{ (file.size / 1024 / 1024).toFixed(2) }} MB</p>
          </div>
        </div>
        <button @click="removeFile(index)" class="p-2 text-slate-500 hover:text-red-400 transition-colors">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
      </div>
    </div>
  </div>
</template>
