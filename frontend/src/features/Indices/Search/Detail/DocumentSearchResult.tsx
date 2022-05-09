import {
    Button,
    Card,
    CardContent,
    CircularProgress,
    Divider,
    Stack,
    Typography,
} from '@mui/material'
import { Fragment } from 'react'
import { FunctionComponent } from 'react'
import { DocumentDto } from '../../indexDtos'
import { DeleteOutline } from '@mui/icons-material'
import DocumentDetailDialog from './DocumentDetailDialog'
import { deleteDocument } from '../indexSearchSlice'
import { useDispatch, useSelector } from 'react-redux'
import { RootState } from '../../../../redux/store'

/**
 * Represents a search result for a document
 */
const DocumentSearchResult = (document: DocumentDto) => {
    const dispatch = useDispatch()
    const deleteLoading = useSelector(
        (state: RootState) => state.indexSearch.deleteLoading
    )
    const { score, text } = document
    return (
        <Stack
            direction="column"
            alignItems="stretch"
            sx={{ minWidth: '100%', maxWidth: '100%' }}
        >
            <Card variant="outlined" sx={{ width: '100%' }}>
                <CardContent>
                    <Typography
                        sx={{ mb: !score ? 1 : 0 }}
                        color="text.secondary"
                        gutterBottom
                    >
                        Document
                    </Typography>
                    {score && (
                        <Fragment>
                            <Stack
                                direction="row"
                                alignItems="baseline"
                                spacing={1}
                            >
                                <Typography fontWeight="bold">
                                    Score:
                                </Typography>
                                <Typography>{score.toFixed(3)}</Typography>
                            </Stack>
                        </Fragment>
                    )}
                    <Typography variant="h6" fontWeight="bold" sx={{ mt: 2 }}>
                        Text
                    </Typography>
                    <Divider sx={{ mb: 1 }} />
                    <Typography
                        variant="body1"
                        sx={{
                            display: '-webkit-box',
                            overflow: 'hidden',
                            WebkitBoxOrient: 'vertical',
                            WebkitLineClamp: 3,
                        }}
                    >
                        {text}
                    </Typography>
                    <Stack
                        direction="row"
                        spacing={1}
                        justifyContent="flex-end"
                        sx={{ mt: 1 }}
                        alignItems="flex-end"
                    >
                        <Button
                            startIcon={<DeleteOutline />}
                            variant="contained"
                            color="error"
                            size="small"
                            disabled={deleteLoading}
                            onClick={() => {
                                dispatch(deleteDocument(document))
                            }}
                        >
                            {deleteLoading && <CircularProgress />}
                            Delete
                        </Button>
                        <DocumentDetailDialog {...document} />
                    </Stack>
                </CardContent>
            </Card>
        </Stack>
    )
}

export default DocumentSearchResult
