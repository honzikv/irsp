import { Stack, Typography } from '@mui/material'
import { FunctionComponent } from 'react'

interface IndicesOverviewProps {
    totalIndices: number
    totalDocuments: number
}

const IndicesOverview: FunctionComponent<IndicesOverviewProps> = ({
    totalIndices,
    totalDocuments,
}) => {
    return (
        <Stack direction="column" justifyContent="flex-end" alignItems="end">
            <Typography align="left" variant="h4" fontWeight="bold">
                Overview
            </Typography>
            <Typography color="text.secondary">Total indices: {totalIndices}</Typography>
            <Typography color="text.secondary">Total documents: {totalDocuments}</Typography>
        </Stack>
    )
}

export default IndicesOverview
