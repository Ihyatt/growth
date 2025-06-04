import { create } from 'zustand';
import { persist } from 'zustand/middleware';

const useAuthStore = create(
  persist(
    (set, get) => ({
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
      
      isAdmin: () => get().permission === 'ADMIN',
      isPractitioner: () => get().permission === 'PRACTITIONER',
      isPatient: () => get().permission === 'PATIENT'
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({ 
        jwtToken: state.jwtToken,
        permission: state.permission,
        isAuthenticated: state.jwtToken !== null
      })
    }
  )
);

export default useAuthStore;