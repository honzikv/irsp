import {
    Button,
    Card,
    CardContent,
    CircularProgress,
    Divider,
    Grid,
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
import ModifyDocumentDialog from './ModifyDocumentDialog'
import ButtonActionConfirmationDialog from '../../../Dialogs/ButtonActionConfirmationDialog'
import DeleteIcon from '@mui/icons-material/Delete'

export interface DocumentSearchResultProps {
    document: DocumentDto
    position: number
}

/**
 * Represents a search_model result for a document
 */
const DocumentSearchResult: FunctionComponent<DocumentSearchResultProps> = ({
    document,
    position,
}) => {
    const dispatch = useDispatch()
    const deleteLoading = useSelector(
        (state: RootState) => state.indexSearch.deleteLoading
    )
    const { score, text } = document
    return (
        <Stack direction="column" alignItems="stretch" sx={{ mb: 1 }}>
            <Card variant="outlined">
                <CardContent sx={{ py: 0.75 }}>
                    <Grid container>
                        <Grid item xs={6} sx={{ mb: 0.5 }}>
                            <Typography
                                sx={{ mb: !score ? 1 : 0 }}
                                color="text.secondary"
                                gutterBottom
                            >
                                #{position}
                            </Typography>
                        </Grid>
                        <Grid item xs={6}>
                            {score && (
                                <Fragment>
                                    <Typography align="right">
                                        <span style={{ fontWeight: 'bold' }}>
                                            Score:
                                        </span>{' '}
                                        {score.toFixed(3)}
                                    </Typography>
                                </Fragment>
                            )}
                        </Grid>
                    </Grid>
                    {document.title && (
                        <Typography
                            variant="h6"
                            fontWeight="bold"
                            sx={{ mt: 2 }}
                        >
                            {document.title}
                        </Typography>
                    )}

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
                        sx={{ mt: 1, pb: 0 }}
                        alignItems="flex-end"
                    >
                        {/* <Button
                            startIcon={<DeleteOutline />}
                            variant="contained"
                            color="error"
                            size="small"
                            disabled={deleteLoading}
                            onClick={() => {
                                dispatch(deleteDocument(document))
                            }}
                        >
                            Delete
                        </Button> */}
                        <ButtonActionConfirmationDialog
                            onConfirm={() => dispatch(deleteDocument(document))}
                            triggerButtonVariant="contained"
                            triggerButtonColor="error"
                            triggerButtonText="Delete"
                            cancelButtonColor="error"
                            title={`Delete document ${document.id}`}
                            buttonSize="small"
                            message={
                                'Are you sure you want to delete this document? This action is irreversible 😨'
                            }
                            StartIcon={DeleteIcon}
                        />
                        <ModifyDocumentDialog
                            variant="modify"
                            documentId={document.id}
                        />
                        <DocumentDetailDialog {...document} />
                    </Stack>
                </CardContent>
            </Card>
        </Stack>
    )
}

export default DocumentSearchResult
