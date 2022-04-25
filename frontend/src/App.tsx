import './App.css'
import { Grid, PaletteMode, Paper, Snackbar } from '@mui/material'
import { createTheme, Theme, ThemeProvider } from '@mui/material/styles'
import { Route, Routes } from 'react-router-dom'
import Home from './features/Home/Home'
import Indices from './features/Indices/Indices'
import Navigation from './features/Navigation/Navigation'
import Header from './features/Navigation/Header'
import { useSelector } from 'react-redux'
import { RootState } from './redux/store'
import { useEffect, useState } from 'react'
import Notification from './features/Notification/Notification'
import IndexDetail from './features/Indices/Search/IndexDetail'

const App = () => {
    const buildTheme = (paletteMode: PaletteMode) =>
        createTheme({
            palette: {
                mode: paletteMode,
            },
            shape: {
                borderRadius: 16
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
                <Notification />
                <Header />
                <Grid container sx={{ mt: 4 }}>
                    <Grid item xs={4} md={2}>
                        <Navigation />
                    </Grid>
                    <Grid item xs={8} md={8}>
                        <Routes>
                            <Route path="/" element={<Home />} />
                            <Route path="/indices" element={<Indices />} />
                            <Route path="/indices/:name" element={<IndexDetail />} />
                        </Routes>
                    </Grid>
                    <Grid item xs={0} md={2} />
                </Grid>
            </Paper>
        </ThemeProvider>
    )
}

export default App
