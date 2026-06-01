import { create } from 'zustand';

interface File {
  id: string;
  filename: string;
  content: string;
}

interface IDEState {
  files: File[];
  activeFileId: string | null;
  output: string;
  isExecuting: boolean;
  setFiles: (files: File[]) => void;
  setActiveFile: (id: string) => void;
  updateFileContent: (id: string, content: string) => void;
  setOutput: (output: string) => void;
  setIsExecuting: (isExecuting: boolean) => void;
}

export const useIDEStore = create<IDEState>((set) => ({
  files: [],
  activeFileId: null,
  output: '',
  isExecuting: false,
  setFiles: (files) => set({ files }),
  setActiveFile: (id) => set({ activeFileId: id }),
  updateFileContent: (id, content) => 
    set((state) => ({
      files: state.files.map(f => f.id === id ? { ...f, content } : f)
    })),
  setOutput: (output) => set({ output }),
  setIsExecuting: (isExecuting) => set({ isExecuting })
}));
