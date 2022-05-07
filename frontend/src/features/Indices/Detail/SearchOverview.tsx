import { Button, Card, CardContent, Stack, Typography } from '@mui/material'
import { Fragment, FunctionComponent, useState } from 'react'
import { DocumentSearchResultDto } from '../indexDtos'
import DownloadIcon from '@mui/icons-material/Download'

export interface SearchOverviewProps {
    model: string
    items: DocumentSearchResultDto[]
}

const SearchOverview: FunctionComponent<SearchOverviewProps> = ({
    model,
    items,
}) => {
    const bestScore = items.length > 0 ? items[0].score : 0
    const worstScore = items.length > 0 ? items[items.length - 1].score : 0

    // Whether the download button should be disabled
    const [downloadButtonDisabled, setDownloadButtonDisabled] = useState(false)

    // Serializes props and saves it to file which the user will be prompted to save
    const downloadAsJson = async () => {
        setDownloadButtonDisabled(true)
        const json = JSON.stringify(items, null, 4)
        const blob = new Blob([json], { type: 'application/json' })
        const href = await URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = href
        link.download = `documents.json`
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        setDownloadButtonDisabled(false)
    }

    return (
        <Fragment>
            <Card variant="outlined" sx={{ minWidth: '100%', my: 2 }}>
                <CardContent>
                    <Stack alignSelf="flex-start">
                        <Typography variant="h4" fontWeight="bold">
                            Overview
                        </Typography>
                        <Typography variant="body1" sx={{ fontSize: 24 }}>
                            Model: {model}
                        </Typography>
                        {items.length === 0}
                        <Typography variant="body1">
                            Total Hits: {items.length}
                        </Typography>
                        <Typography variant="body1">
                            Best Score: {bestScore?.toFixed(3) ?? 0}
                        </Typography>
                        <Typography variant="body1">
                            Worst Score: {worstScore?.toFixed(3) ?? 0}
                        </Typography>
                    </Stack>
                    <Stack
                        sx={{ ml: 'auto', mt: 2, minWidth: '0%' }}
                        alignItems="flex-end"
                        alignSelf="flex-end"
                        justifyContent="flex-end"
                    >
                        <Button
                            startIcon={<DownloadIcon />}
                            disabled={downloadButtonDisabled}
                            onClick={downloadAsJson}
                            variant="contained"
                        >
                            Download all as JSON
                        </Button>
                    </Stack>
                </CardContent>
            </Card>
        </Fragment>
    )
}

export default SearchOverview
