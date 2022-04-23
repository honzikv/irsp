import { AppBar, Box, IconButton, Toolbar, Typography } from '@mui/material'
import { useDispatch, useSelector } from 'react-redux'
import { RootState } from '../../redux/store'
import DarkModeIcon from '@mui/icons-material/DarkMode'
import { toggleTheme } from '../theme/themeSlice'
import LightModeIcon from '@mui/icons-material/LightMode'

const Header = () => {
    const colorThemeMode = useSelector(
        (state: RootState) => state.theme.paletteMode
    )

    const dispatch = useDispatch()

    const onToggleTheme = () => {
        dispatch(toggleTheme())
    }

    return (
        <Box sx={{ flexGrow: 1 }}>
            <AppBar position="static">
                <Toolbar>
                    <Typography
                        variant="h5"
                        fontWeight="bold"
                        // component="div"
                        sx={{ flexGrow: 1 }}
                    >
                        IR Search App
                    </Typography>
                    {colorThemeMode === 'dark' ? (
                        <IconButton onClick={onToggleTheme}>
                            <LightModeIcon />
                        </IconButton>
                    ) : (
                        <IconButton onClick={onToggleTheme}>
                            <DarkModeIcon />
                        </IconButton>
                    )}
                </Toolbar>
            </AppBar>
        </Box>
    )
}

export default Header
