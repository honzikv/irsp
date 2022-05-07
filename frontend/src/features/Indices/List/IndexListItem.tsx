import {
    Avatar,
    Button,
    Card,
    CardContent,
    ListItem,
    ListItemAvatar,
    ListItemText,
    Stack,
    Typography,
} from '@mui/material'
import { Fragment, FunctionComponent } from 'react'
import { useDispatch } from 'react-redux'
import axiosInstance from '../../../conf/axios'
import ButtonActionConfirmationDialog from '../../Dialogs/ButtonActionConfirmationDialog'
import { showNotification } from '../../Notification/notificationSlice'
import { IndexDto } from '../indexDtos'
import { fetchIndices } from '../indicesSlice'
import { Link as RouterLink } from 'react-router-dom'
import SearchIcon from '@mui/icons-material/Search'
import DeleteIcon from '@mui/icons-material/Delete'

const IndexListItem: FunctionComponent<IndexDto> = ({
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
            {/* <ListItem> */}
            <CardContent>
                <Stack direction="column" alignItems="stretch">
                    <Stack direction="row" alignItems="center">
                        <ListItemAvatar>
                            <Avatar>
                                {name.substring(0, Math.min(name.length, 2))}
                            </Avatar>
                        </ListItemAvatar>
                        <ListItemText
                            primary={
                                <Typography variant="h6">{name}</Typography>
                            }
                            secondary={
                                <Fragment>
                                    <Typography
                                        sx={{ display: 'inline' }}
                                        component="span"
                                        variant="body1"
                                        color="text.primary"
                                    >
                                        {nDocs} documents,
                                    </Typography>
                                    {` containing ${nTerms} terms`}
                                </Fragment>
                            }
                        />
                    </Stack>
                    <Stack
                        direction="row"
                        justifyContent="flex-end"
                        alignItems="center"
                        alignSelf="flex-end"
                        sx={{ mt: 0.5, ml: 'auto' }}
                        spacing={2}
                    >
                        <ButtonActionConfirmationDialog
                            onConfirm={deleteIndex}
                            triggerButtonVariant="contained"
                            triggerButtonColor="error"
                            triggerButtonText="Delete"
                            cancelButtonColor="error"
                            title={`Delete index ${name}`}
                            buttonSize="small"
                            message={
                                'Are you sure you want to delete this index? This action is irreversible and all indexed documents will be lost.'
                            }
                            StartIcon={DeleteIcon}
                        />
                        <Button
                            component={RouterLink}
                            startIcon={<SearchIcon />}
                            variant="contained"
                            size="small"
                            to={`/indices/${name}`}
                        >
                            Search
                        </Button>
                    </Stack>
                </Stack>
            </CardContent>
        </Card>
    )
}

export default IndexListItem
