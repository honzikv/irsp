import { Container, Link, Stack, Typography } from '@mui/material'
import { Fragment } from 'react'
import { Link as RouterLink } from 'react-router-dom'
const Home = () => {
    return (
        <Fragment>
            <Stack alignItems="center" justifyContent="center">
                <Container sx={{ mt: 'auto', mb: 'auto' }}>
                    <Typography variant="h3" fontWeight="bold">
                        IR Search Engine
                    </Typography>
                    <Typography sx={{ fontSize: '24px' }}>
                        A simple search app.
                    </Typography>
                    <Link component={RouterLink} to="/indices">
                        Indices
                    </Link>
                </Container>
            </Stack>
        </Fragment>
    )
}

export default Home
