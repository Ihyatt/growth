import { create } from 'zustand';
import { persist } from 'zustand/middleware';

const useAuthStore = create(
  persist(
    (set, get) => ({ // 👈 Add 'get' here
      jwtToken: null,
      permission: null,
      isAuthenticated: false,
      
      login: (jwtToken, permission) => {
        set({ 
          jwtToken,
          permission,
          isAuthenticated: true 
        });
      },
      
      logout: () => {
        set({ 
          jwtToken: null,
          permission: null,
          isAuthenticated: false 
        });
      },
      
      // Fixed helper functions
      isAdmin: () => get().permission === 'ADMIN', // ✅ Now works
      isPractitioner: () => get().permission === 'PRACTITIONER',
      isPatient: () => get().permission === 'PATIENT'
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({ 
        jwtToken: state.jwtToken,
        permission: state.permission 
      })
    }
  )
);

export default useAuthStore;