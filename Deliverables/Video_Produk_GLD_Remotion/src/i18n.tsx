import React, {createContext, useContext} from 'react';
import type {Lang} from './timeline';

// Bahasa aktif komposisi (ID/EN). Komponen memakai `const t = useT(); t('teks ID', 'English text')`.
const LangContext = createContext<Lang>('id');
export const LangProvider: React.FC<{lang: Lang; children: React.ReactNode}> = ({lang, children}) => (
  <LangContext.Provider value={lang}>{children}</LangContext.Provider>
);
export const useLang = () => useContext(LangContext);
export const useT = () => {
  const lang = useLang();
  return (id: string, en: string) => (lang === 'en' ? en : id);
};
