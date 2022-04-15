import {
    Button,
    Link,
    List,
    ListItem,
    ListItemIcon,
    ListItemText,
    SvgIconTypeMap,
} from '@mui/material'
import { Fragment } from 'react'
import HomeIcon from '@mui/icons-material/Home'
import ListIcon from '@mui/icons-material/List'
import { Link as RouterLink } from 'react-router-dom'
import { OverridableComponent } from '@mui/material/OverridableComponent'

interface MenuItem {
    label: string
    path: string
    icon: OverridableComponent<SvgIconTypeMap<{}, 'svg'>>
}

const menuItems: MenuItem[] = [
    {
        label: 'Home',
        path: '/',
        icon: HomeIcon,
    },
    {
        label: 'Indices',
        path: '/indices',
        icon: ListIcon,
    },
]

const Navigation = () => {
    return (
        <Fragment>
            <List sx={{pl: 4}}>
                {menuItems.map((item, idx) => (
                    <Link
                        underline="none"
                        color="inherit"
                        component={RouterLink}
                        to={item.path}
                        key={idx}
                    >
                        <ListItem button>
                            <ListItemIcon>
                                <item.icon />
                            </ListItemIcon>
                            <ListItemText>{item.label}</ListItemText>
                        </ListItem>
                    </Link>
                ))}
            </List>
        </Fragment>
    )
}

export default Navigation
