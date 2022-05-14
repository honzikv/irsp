import {
    Button,
    Card,
    CardContent,
    Divider,
    Grid,
    Stack,
    Typography,
} from '@mui/material'
import { Fragment, useEffect, useState } from 'react'
import DownloadIcon from '@mui/icons-material/Download'
import { RootState } from '../../../redux/store'
import { useDispatch, useSelector } from 'react-redux'
import { showNotification } from '../../Notification/notificationSlice'

const mapModelToDisplayString = (model: string) => {
    switch (model) {
        case 'tfidf':
            return 'TF-IDF'
        case 'bool':
            return 'Boolean'
        default:
            return 'BM25'
    }
}

const SearchOverview = () => {
    const [bestScore, setBestScore] = useState<number | undefined>(undefined)
    const [worstScore, setWorstScore] = useState<number | undefined>(undefined)
    const [totalHits, setTotalHits] = useState<number | undefined>(undefined)
    const [modelName, setModelName] = useState<string | undefined>(undefined)

    const dispatch = useDispatch()

    const documents = useSelector(
        (state: RootState) => state.indexSearch.documents
    )
    const totalDocuments = useSelector(
        (state: RootState) => state.indexSearch.totalDocuments
    )
    const query = useSelector((state: RootState) => state.indexSearch.query)
    const stopwords = useSelector((state: RootState) => state.indexSearch.stopwords)

    const resetState = () => {
        setBestScore(undefined)
        setWorstScore(undefined)
        setTotalHits(undefined)
    }

    useEffect(() => {
        resetState()
        if (!query || !documents) {
            return
        }

        const model = query.model ?? 'tfidf'
        setModelName(mapModelToDisplayString(model))
        setTotalHits(totalDocuments)

        if (documents.length === 0) {
            dispatch(
                showNotification({
                    message: 'No results matching this query were found',
                    severity: 'warning',
                    autohideSecs: 5,
                })
            )
            return
        }

        // Do not display "best score" and "worst score" if the model is boolean since its unranked
        if (model === 'bool') {
            return
        }

        // Items are ordered in descending order, so the first one is the best
        setBestScore(documents[0].score)
        // The last one is the worst
        setWorstScore(documents[documents.length - 1].score)
    }, [dispatch, query, documents, totalDocuments])

    // Whether the download button should be disabled
    const [downloadButtonDisabled, setDownloadButtonDisabled] = useState(false)

    // Serializes props and saves it to file which the user will be prompted to save
    const downloadAsJson = () => {
        setDownloadButtonDisabled(true)
        const json = JSON.stringify(documents ?? [], null, 4)
        const blob = new Blob([json], { type: 'application/json' })
        const href = URL.createObjectURL(blob)
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
            <Card variant="outlined" sx={{ minWidth: '100%', mb: 1 }}>
                <CardContent sx={{ py: 0.75 }}>
                    <Grid
                        container
                        // alignSelf="flex-start"
                        // alignItems="stretch"
                        justifyContent="space-between"
                        spacing={2}
                        // sx={{ mx: 4 }}
                        direction="row"
                    >
                        <Grid item xs={12} md={6}>
                            <Typography variant="h4" fontWeight="bold">
                                Overview
                            </Typography>
                            {modelName && (
                                <Typography
                                    variant="body1"
                                    sx={{ fontSize: 16 }}
                                >
                                    Model: {modelName}
                                </Typography>
                            )}
                        </Grid>
                        <Grid item xs={12} md={6}>
                            {totalHits !== undefined && (
                                <Typography variant="body1" align="right">
                                    Total Hits: {totalHits}
                                </Typography>
                            )}
                            {bestScore && (
                                <Typography variant="body1" align="right">
                                    Best Score: {bestScore.toFixed(3)}
                                </Typography>
                            )}
                            {worstScore && (
                                <Typography variant="body1" align="right">
                                    Worst Score: {worstScore.toFixed(3)}
                                </Typography>
                            )}
                        </Grid>
                    </Grid>
                    {
                        // Only show the download button if the user has results
                        documents && documents.length > 0 && (
                            <Stack
                                alignItems="center"
                                alignSelf="flex-end"
                                justifyContent="space-between"
                                direction="row"
                                sx={{mt: 1}}
                                spacing={1}
                            >
                                {(
                                    <Typography align="left" color="error">
                                        { stopwords && stopwords.length > 0 && `Stopwords detected during search: "${stopwords.join(', ')}"`}{' '}
                                    </Typography>
                                )}

                                <Button
                                    startIcon={<DownloadIcon />}
                                    disabled={downloadButtonDisabled}
                                    onClick={downloadAsJson}
                                    variant="contained"
                                    size="small"
                                >
                                    Download all as JSON
                                </Button>
                            </Stack>
                        )
                    }
                </CardContent>
            </Card>
            {totalHits && totalHits > 0 ? (
                <Divider sx={{ mb: 1 }} />
            ) : (
                <Typography color="primary" align="center">
                    No items matching this query were found
                </Typography>
            )}
        </Fragment>
    )
}

export default SearchOverview
