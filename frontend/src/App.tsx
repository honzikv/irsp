import './App.css'
import { Grid, PaletteMode, Paper, Snackbar } from '@mui/material'
import { createTheme, PaletteColor, Theme, ThemeProvider } from '@mui/material/styles'
import { Route, Routes } from 'react-router-dom'
import Home from './features/Home/Home'
import Indices from './features/Indices/Indices'
import Navigation from './features/Navigation/Navigation'
import Header from './features/Navigation/Header'
import { useSelector } from 'react-redux'
import { RootState } from './redux/store'
import { useEffect, useState } from 'react'
import Notification from './features/Notification/Notification'
import IndexSearch from './features/Indices/Search/IndexSearch'

const App = () => {

    const lightThemePalette = {
        primary: {
            main: '#5260ff',
            dark: '#3171e0',
            light: '#4c8dff'
        },
        secondary: {
            main: '#5D6B73',
            dark: '#56646C',
            light: '#6D7F89',
        },
        success: {
            main: '#2dd36f',
            dark: '#28ba62',
            light: '#42d77d',
        },
        warning: {
            main: '#ffc409',
            dark: '#e0ac08',
            light: '#ffca22'
        },
        error: {
            main: '#eb445a',
            dark: '#cf3c4f',
            light: '#ed576b'
        }
    }

    const darkThemePalette = {
        primary: {
            main: '#3dc2ff',
            dark: '#36abe0',
            light: '#50c8ff',
        },
    }

    const getPalette = (paletteMode: PaletteMode) => {
        switch (paletteMode) {
            case 'light':
                return lightThemePalette
            case 'dark':
                return darkThemePalette
            default:
                return lightThemePalette
        }
    }

    const buildTheme = (paletteMode: PaletteMode) =>
        createTheme({
            palette: {
                mode: paletteMode,
                ...getPalette(paletteMode),
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
                    <Grid item xs={12} md={8} sx={{mx: .5}}>
                        <Routes>
                            <Route path="/" element={<Home />} />
                            <Route path="/indices" element={<Indices />} />
                            <Route path="/indices/:name" element={<IndexSearch />} />
                        </Routes>
                    </Grid>
                    <Grid item xs={0} md={2} />
                </Grid>
            </Paper>
        </ThemeProvider>
    )
}

export default App
