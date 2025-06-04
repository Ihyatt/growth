import { create } from 'zustand';
import { persist } from 'zustand/middleware';

const useAuthStore = create(
  persist(
    (set) => ({
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
      
      // Helper functions
      isAdmin: () => get().permission === 'ADMIN',
      isPractitioner: () => get().permission === 'PRACTITIONER',
      isPatient: () => get().permission === 'PATIENT'
    }),
    {
      name: 'auth-storage', // localStorage key
      partialize: (state) => ({ 
        jwtToken: state.jwtToken,
        permission: state.permission 
      })
    }
  )
);

export default useAuthStore;