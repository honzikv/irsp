import { createSlice } from '@reduxjs/toolkit'
import { persistReducer } from 'redux-persist'
import storage from 'redux-persist/lib/storage'
import { Theme } from '@mui/material/styles'
import { PaletteMode } from '@mui/material'

export interface ThemeState {
    paletteMode: PaletteMode
}

const persistConfig = {
    key: 'theme',
    storage, // localStorage for browsers
}

const initialState: ThemeState = {
    paletteMode: 'light',
}

const themeSlice = createSlice({
    name: 'theme',
    initialState,
    reducers: {
        toggleTheme: (state: any) => ({
            ...state,
            paletteMode: state.paletteMode === 'light' ? 'dark' : 'light',
        }),
    },
})

const themeReducer = persistReducer(persistConfig, themeSlice.reducer)
// const themeReducer = themeSlice.reducer
export const { toggleTheme } = themeSlice.actions
export default themeReducer
