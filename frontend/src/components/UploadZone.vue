<script setup lang="ts">
import { ref, watch } from 'vue'
import { 
  CloudUpload, 
  File, 
  FileText, 
  X,
  CheckCircle2
} from 'lucide-vue-next'

const emit = defineEmits(['update:files'])

const isDragging = ref(false)
const files = ref<File[]>([])

watch(files, (newFiles) => {
  emit('update:files', newFiles)
}, { deep: true })

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
      class="border-4 border-dashed rounded-[2.5rem] p-20 text-center transition-all duration-500 group relative overflow-hidden shadow-inner"
      :class="isDragging ? 'border-primary bg-primary/10' : 'border-[var(--border-main)] bg-[var(--surface-1)] hover:border-primary/50'"
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
      
      <div v-if="isDragging" class="absolute inset-0 flex items-center justify-center bg-primary/5 backdrop-blur-[2px] pointer-events-none">
         <CheckCircle2 class="w-24 h-24 text-primary animate-bounce shadow-2xl" />
      </div>

      <label for="fileInput" class="cursor-pointer">
        <div class="flex flex-col items-center">
          <div class="w-28 h-28 bg-primary/10 rounded-[2rem] flex items-center justify-center mb-10 group-hover:scale-110 group-hover:rotate-6 transition-all border border-primary/20 shadow-xl shadow-primary/5">
            <CloudUpload class="w-14 h-14 text-primary" />
          </div>
          <h3 class="text-3xl font-black text-[var(--text-heading)] tracking-tighter">Upload Financial Documents</h3>
          <p class="text-[var(--text-main)] mt-4 font-medium opacity-70">PDF, CSV, or XML files. Max 50MB per file.</p>
          <div class="mt-10 px-10 py-4 bg-primary hover:bg-primary-hover rounded-2xl text-white font-black transition-all shadow-2xl shadow-primary/20 active:scale-95 uppercase tracking-widest text-xs">
            Browse Documents
          </div>
        </div>
      </label>
    </div>

    <!-- File List -->
    <div v-if="files.length > 0" class="mt-16 space-y-5">
      <div class="flex items-center justify-between px-4">
        <div class="flex items-center gap-3">
          <div class="w-2 h-2 rounded-full bg-primary"></div>
          <h4 class="text-[10px] font-black text-[var(--text-label)] uppercase tracking-[0.2em]">Selected Documents ({{ files.length }})</h4>
        </div>
        <button @click="files = []" class="text-[10px] font-black text-[var(--color-danger)] uppercase tracking-widest hover:underline transition-all">Clear All</button>
      </div>
      <div v-for="(file, index) in files" :key="index" class="group flex items-center justify-between p-6 bg-[var(--surface-raised)] rounded-[2rem] border border-[var(--border-main)] shadow-sm hover:border-primary/40 hover:shadow-2xl hover:shadow-primary/5 transition-all">
        <div class="flex items-center gap-6">
          <div class="w-14 h-14 rounded-2xl flex items-center justify-center border transition-all group-hover:scale-110 shadow-sm" 
               :class="file.type === 'application/pdf' ? 'bg-[var(--color-danger-muted)] border-[var(--color-danger)]/20 text-[var(--color-danger)]' : 'bg-[var(--color-success-muted)] border-[var(--color-success)]/20 text-[var(--color-success)]'">
            <FileText v-if="file.type === 'application/pdf'" class="w-7 h-7" />
            <File v-else class="w-7 h-7" />
          </div>
          <div>
            <p class="text-base font-black text-[var(--text-heading)] group-hover:text-primary transition-colors tracking-tight">{{ file.name }}</p>
            <p class="text-[11px] font-black text-[var(--text-muted)] mt-1.5 tracking-tighter uppercase opacity-60">{{ (file.size / 1024 / 1024).toFixed(2) }} MB</p>
          </div>
        </div>
        <button @click="removeFile(index)" class="p-4 text-[var(--text-muted)] hover:text-[var(--color-danger)] bg-[var(--surface-2)] hover:bg-[var(--color-danger-muted)] rounded-2xl transition-all active:scale-75 border border-[var(--border-main)]/50">
          <X class="w-6 h-6" />
        </button>
      </div>
    </div>
  </div>
</template>
