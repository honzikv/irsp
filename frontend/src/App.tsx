import './App.css'
import { Grid, PaletteMode, Paper } from '@mui/material'
import { createTheme, Theme, ThemeProvider } from '@mui/material/styles'
import { Route, Routes } from 'react-router-dom'
import Home from './features/Home/Home'
import Indices from './features/Indices/Indices'
import Navigation from './features/Navigation/Navigation'
import Header from './features/Navigation/Header'
import { useSelector } from 'react-redux'
import { RootState } from './redux/store'
import { Fragment, useEffect, useState } from 'react'

const App = () => {
    const buildTheme = (paletteMode: PaletteMode) =>
        createTheme({
            palette: {
                mode: paletteMode,
            },
            typography: {
                fontFamily: [
                    '-apple-system',
                    'BlinkMacSystemFont',
                    '"Segoe UI"',
                    'Roboto',
                    '"Helvetica Neue"',
                    'Arial',
                    'sans-serif',
                    '"Apple Color Emoji"',
                    '"Segoe UI Emoji"',
                    '"Segoe UI Symbol"',
                ].join(','),
            },
        })

    const paletteMode = useSelector(
        (state: RootState) => state.theme.paletteMode
    )

    const [theme, setTheme] = useState<Theme>(buildTheme(paletteMode))
    useEffect(() => {
        setTheme(() => {
            return buildTheme(paletteMode)
        })
    }, [paletteMode])

    return (
        <ThemeProvider theme={theme}>
            <Paper style={{ minHeight: '100vh', borderRadius: 0 }}>
                <Header />
                <Grid container sx={{ mt: 4 }}>
                    <Grid item xs={2}>
                        <Navigation />
                    </Grid>
                    <Grid item xs={10}>
                        <Routes>
                            <Route path="/" element={<Home />} />
                            <Route path="/indices" element={<Indices />} />
                        </Routes>
                    </Grid>
                </Grid>
            </Paper>
        </ThemeProvider>
    )
}

export default App
