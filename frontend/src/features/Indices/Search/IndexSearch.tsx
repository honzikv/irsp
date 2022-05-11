import {
    CircularProgress,
    FormControl,
    Grid,
    IconButton,
    InputBase,
    InputLabel,
    MenuItem,
    Paper,
    Select,
    SelectChangeEvent,
    Stack,
    Typography,
} from '@mui/material'
import { useFormik } from 'formik'
import { Fragment, useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { useNavigate, useParams } from 'react-router-dom'
import SearchIcon from '@mui/icons-material/Search'
import DocumentSearchResult from './Detail/DocumentSearchResult'
import SearchOverview from './SearchOverview'
import { showNotification } from '../../Notification/notificationSlice'
import UploadDocumentJsonDialog from './Detail/UploadDocumentsDialog'
import { RootState } from '../../../redux/store'
import {
    clear,
    clearSearchResult,
    consumeErr,
    search,
    setIndex,
    setQuery,
    consumeDeleteSuccess,
} from './indexSearchSlice'
import ModifyDocumentDialog from './Detail/ModifyDocumentDialog'

const initialValues = {
    query: '',
    model: 'tfidf',
    // topK: 10,
}

// Detail component which shows the search_model bar, results and some configuration
const IndexSearch = () => {
    const dispatch = useDispatch()

    // name of the index
    const { name } = useParams()
    const navigate = useNavigate()

    // Search result
    const searchResult = useSelector(
        (state: RootState) => state.indexSearch.searchResult
    )

    // Whether the search_model is loading something from the API
    const loading = useSelector((state: RootState) => state.indexSearch.loading)
    const err = useSelector((state: RootState) => state.indexSearch.err)
    const deleteLoading = useSelector(
        (state: RootState) => state.indexSearch.deleteLoading
    )
    const deleteSuccess = useSelector(
        (state: RootState) => state.indexSearch.deleteSuccess
    )

    // UseEffect to redirect user if the URI is invalid
    useEffect(() => {
        if (!name) {
            navigate('/')
        }

        // Clear the state
        dispatch(clear())

        // Set the index
        dispatch(setIndex(name))

        // If the component is unmounting clear the state as well
        return () => {
            dispatch(clear())
        }
    }, [name, navigate, dispatch])

    // UseEffect to show error message if there is an error
    useEffect(() => {
        if (err) {
            dispatch(
                showNotification({
                    message: err,
                    severity: 'error',
                })
            )
            dispatch(consumeErr())
        }
    }, [err, dispatch])

    const formik = useFormik({
        initialValues,
        onSubmit: async (values) => {
            dispatch(clearSearchResult()) // clear search_model result
            // set the query
            dispatch(
                setQuery({
                    ...values,
                    model: values.model,
                })
            )
            // and begin searching
            dispatch(search())
        },
    })

    useEffect(() => {
        if (!deleteLoading && deleteSuccess) {
            dispatch(
                showNotification({ message: 'Document deleted successfully' })
            )
            dispatch(consumeDeleteSuccess())
        }
    }, [dispatch, deleteLoading, deleteSuccess])

    return (
        <Fragment>
            <Grid container spacing={1} justifyContent="center">
                <Grid item xs={0} md={1} lg={2} />
                <Grid item xs={12} md={10} lg={8}>
                    <Fragment>
                        <Typography
                            sx={{ mt: 1, mb: 2 }}
                            variant="h3"
                            fontWeight="bold"
                        >
                            {name}
                        </Typography>
                        <form onSubmit={formik.handleSubmit}>
                            <Grid
                                container
                                spacing={2}
                                direction="row"
                                justifyContent="space-around"
                                alignItems="center"
                                alignSelf="stretch"
                            >
                                <Grid item xs={12} md={3}>
                                    <FormControl fullWidth>
                                        <InputLabel id="searchModelLabel">
                                            Search Model
                                        </InputLabel>
                                        <Select
                                            labelId="searchModelLabel"
                                            id="searchModel"
                                            value={formik.values.model}
                                            onChange={(
                                                event: SelectChangeEvent
                                            ) => {
                                                formik.setFieldValue(
                                                    'model',
                                                    event.target.value
                                                )
                                            }}
                                            label="SearchModel"
                                        >
                                            <MenuItem value="tfidf">
                                                TF-IDF
                                            </MenuItem>
                                            <MenuItem value="bool">
                                                Bool
                                            </MenuItem>
                                            <MenuItem value="transformers">
                                                Transformers 🚗
                                            </MenuItem>
                                        </Select>
                                    </FormControl>
                                </Grid>
                                <Grid item xs={12} md={9}>
                                    <Paper
                                        variant="outlined"
                                        sx={{
                                            p: '2px 4px',
                                            alignItems: 'center',
                                            display: 'flex',
                                        }}
                                    >
                                        <InputBase
                                            sx={{ ml: 1, flex: 1 }}
                                            placeholder="Search Index"
                                            value={formik.values.query}
                                            onChange={(e: any) => {
                                                formik.setFieldValue(
                                                    'query',
                                                    e.target.value
                                                )
                                            }}
                                            inputProps={{
                                                'aria-label': 'search',
                                            }}
                                        />
                                        <IconButton
                                            type="submit"
                                            sx={{ p: '10px' }}
                                            aria-label="search"
                                        >
                                            <SearchIcon />
                                        </IconButton>
                                    </Paper>
                                </Grid>
                            </Grid>
                        </form>

                        {name && (
                            <Stack
                                alignSelf="flex-end"
                                alignItems="flex-end"
                                justifyContent="flex-end"
                                direction="row"
                                spacing={2}
                                sx={{ my: 2 }}
                            >
                                <ModifyDocumentDialog variant="create" />
                                <UploadDocumentJsonDialog />
                            </Stack>
                        )}
                        {searchResult && <SearchOverview />}

                        <Stack
                            direction="column"
                            justifyContent="center"
                            alignItems="stretch"
                            alignSelf="stretch"
                            spacing={1}
                        >
                            {searchResult &&
                                searchResult.documents.map((doc, idx) => (
                                    <DocumentSearchResult
                                        key={idx}
                                        {...doc}
                                    />
                                ))}
                            {loading && (
                                <Stack
                                    alignItems="center"
                                    justifyContent="center"
                                >
                                    <CircularProgress />
                                </Stack>
                            )}
                        </Stack>
                    </Fragment>
                </Grid>
                <Grid item xs={0} md={1} lg={2} />
            </Grid>
        </Fragment>
    )
}

export default IndexSearch
