import { CircularProgress, Stack, Typography } from '@mui/material'
import { Fragment } from 'react'

/**
 * Component that shows a skeleton while the specified item is loading
 * @returns
 */
const ContentLoading = () => (
    <Fragment>
        <Typography align="center" fontWeight={400}>
            Loading ...
        </Typography>
        <Stack sx={{ mt: 2 }} justifyContent="center" alignItems="center">
            <CircularProgress />
        </Stack>
    </Fragment>
)

export default ContentLoading
