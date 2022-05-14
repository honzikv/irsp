import {
    Button,
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
import { Fragment, useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { useNavigate, useParams } from 'react-router-dom'
import SearchIcon from '@mui/icons-material/Search'
import SearchOverview from './SearchOverview'
import { showNotification } from '../../Notification/notificationSlice'
import UploadDocumentJsonDialog from './Documents/UploadDocumentJsonDialog'
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
import ModifyDocumentDialog from './Documents/ModifyDocumentDialog'
import VirtualizedDocumentList from './Documents/VirtualizedDocumentList'

// Detail component which shows the search_model bar, results and some configuration
const IndexSearch = () => {
    const dispatch = useDispatch()

    // name of the index
    const { name } = useParams()
    const navigate = useNavigate()

    // Loaded documents
    const documents = useSelector((state: RootState) => state.indexSearch.documents)

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
        initialValues: {
            query: '',
            model: 'tfidf',
            topK: 'all',
        },

        onSubmit: async (values) => {
            dispatch(clearSearchResult()) // clear search_model result
            // set the query
            dispatch(
                setQuery({
                    ...values,
                    model: values.model,
                    topK: values.topK === 'all' ? undefined : values.topK,
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
                                alignItems="start"
                                alignSelf="stretch"
                            >
                                <Grid item xs={12} md={3}>
                                    <FormControl fullWidth sx={{ mb: 2 }}>
                                        <InputLabel id="searchModelLabel">
                                            Search Model
                                        </InputLabel>
                                        <Select
                                            size="small"
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
                                            <MenuItem value="bm25">
                                                BM25
                                            </MenuItem>
                                        </Select>
                                    </FormControl>
                                    <FormControl fullWidth >
                                    <InputLabel id="topKLabel">
                                            Max number of results
                                        </InputLabel>
                                        <Select
                                            labelId="topKLabel"
                                            id="topK"
                                            size="small"
                                            value={formik.values.topK}
                                            onChange={(
                                                event: SelectChangeEvent
                                            ) => {
                                                formik.setFieldValue(
                                                    'topK',
                                                    event.target.value
                                                )
                                            }}
                                            label="Max number of results"
                                        >
                                            <MenuItem value="all">
                                                All
                                            </MenuItem>
                                            <MenuItem value={10}>10</MenuItem>
                                            <MenuItem value={50}>50</MenuItem>
                                            <MenuItem value={100}>100</MenuItem>
                                            <MenuItem value={200}>200</MenuItem>
                                        </Select>
                                    </FormControl>
                                </Grid>
                                <Grid item xs={12} md={9}>
                                    <Paper
                                        variant="outlined"
                                        sx={{
                                            p: '4px 4px',
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
                                        <Button
                                            aria-label="search"
                                            color="inherit"
                                            type="submit"
                                            endIcon={<SearchIcon />}
                                        >
                                            Search
                                        </Button>
                                        {/* <IconButton
                                            type="submit"
                                            sx={{ p: '10px' }}
                                            aria-label="search"
                                        >
                                            Search
                                            <SearchIcon />
                                        </IconButton> */}
                                    </Paper>
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
                                </Grid>
                            </Grid>
                        </form>

                        {documents && <SearchOverview />}

                        <Stack
                            direction="column"
                            justifyContent="center"
                            alignItems="stretch"
                            alignSelf="stretch"
                            spacing={1}
                        >
                            <VirtualizedDocumentList />
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
