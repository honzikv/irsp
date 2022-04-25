import { Button, Card, CardContent, Stack, Typography } from '@mui/material'
import { FunctionComponent } from 'react'
import { useDispatch } from 'react-redux'
import axiosInstance from '../../conf/axios'
import ButtonActionConfirmationDialog from '../Dialogs/ButtonActionConfirmationDialog'
import { showNotification } from '../Notification/notificationSlice'
import { IndexDto } from './indicesDtos'
import { fetchIndices } from './indicesSlice'
import { Link as RouterLink } from 'react-router-dom'
import SearchIcon from '@mui/icons-material/Search'
import DeleteIcon from '@mui/icons-material/Delete'

const IndexCardDetail: FunctionComponent<IndexDto> = ({
    name,
    nDocs,
    nTerms,
}) => {
    const dispatch = useDispatch()

    const deleteIndex = async () => {
        try {
            const { data } = await axiosInstance.delete(`/indices/${name}`)
            if (data.success) {
                dispatch(
                    showNotification({
                        message: data.message,
                        type: 'success',
                        autohideSecs: 5,
                    })
                )
            } else {
                dispatch(
                    showNotification({
                        message: data.message,
                        type: 'error',
                        autohideSecs: 5,
                    })
                )
            }
        } catch (err: any) {
            dispatch(
                showNotification({
                    message: 'Error while communicating with the server',
                    type: 'error',
                    autohideSecs: 5,
                })
            )
        }
        dispatch(fetchIndices())
    }

    return (
        <Card variant="outlined">
            <CardContent>
                <Typography variant="h5" fontWeight="bold">
                    {name}
                </Typography>
                <Typography color="text.secondary">{nTerms} terms</Typography>
                <Typography color="text.secondary">
                    {nDocs} documents
                </Typography>
                <Stack
                    direction="row"
                    justifyContent="flex-end"
                    alignItems="center"
                    spacing={1}
                >
                    <ButtonActionConfirmationDialog
                        onConfirm={deleteIndex}
                        triggerButtonVariant="contained"
                        triggerButtonColor="error"
                        triggerButtonText="Delete"
                        cancelButtonColor="error"
                        title={`Delete index ${name}`}
                        message={
                            'Are you sure you want to delete this index? This action is irreversible and all indexed documents will be lost.'
                        }
                        StartIcon={DeleteIcon}
                    />
                    <Button component={RouterLink} startIcon={<SearchIcon />} variant="contained" to={`/indices/${name}`}>Search</Button>
                </Stack>
            </CardContent>
        </Card>
    )
}

export default IndexCardDetail
