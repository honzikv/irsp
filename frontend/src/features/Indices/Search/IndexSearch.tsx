import {
    Divider,
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
import { Fragment, useState } from 'react'
import { useDispatch } from 'react-redux'
import { useParams } from 'react-router-dom'
import SearchIcon from '@mui/icons-material/Search'
import DocumentSearchResult from './DocumentSearchResult'
import { DocumentSearchResultDto } from '../indicesDtos'
import SearchOverview from './SearchOverview'
import axiosInstance from '../../../conf/axios'
import { showNotification } from '../../Notification/notificationSlice'

// Detail component which shows the search bar, results and some configuration
const IndexSearch = () => {
    const dispatch = useDispatch()
    const { name } = useParams()

    const [model, setModel] = useState<string | undefined>(undefined)
    const [searchSuccessful, setSearchSuccessful] = useState(false)
    const [documents, setDocuments] = useState<DocumentSearchResultDto[]>([])

    const mapModelToDisplayString = (model: string) => {
        switch (model) {
            case 'tfidf':
                return 'TF-IDF'
            case 'transformers':
                return 'Transformers'
            default:
                return 'Boolean'
        }
    }

    const initialValues = {
        query: '',
        model: 'tfidf',
        topK: 10,
    }

    const formik = useFormik({
        initialValues,
        onSubmit: async (values) => {
            try {
                const { data } = await axiosInstance.post(
                    `/indices/${name}/search`,
                    {
                        query: values.query,
                        model: values.model,
                    }
                )

                if (!data.success) {
                    dispatch(
                        showNotification({
                            message:
                                data.message ??
                                'Unknown error occurred, please try again later.',
                            type: 'error',
                            autohideSecs: 5,
                        })
                    )
                    setSearchSuccessful(false)
                    setModel(undefined)
                    return
                }

                console.log(data)

                setModel(mapModelToDisplayString(values.model))
                setDocuments(data.message ?? ([] as DocumentSearchResultDto[]))
                setSearchSuccessful(true)
            } catch (err: any) {
                dispatch(
                    showNotification({
                        message: 'Error while communicating with the server',
                        type: 'error',
                        autohideSecs: 5,
                    })
                )
            }
        },
    })

    return (
        <Fragment>
            <Grid container spacing={1}>
                <Grid item xs={0} md={1} lg={2} />
                <Grid item xs={12} md={10} lg={8}>
                    <Stack alignItems="Center">
                        <Typography
                            sx={{ mt: 1, mb: 2 }}
                            variant="h3"
                            fontWeight="bold"
                        >
                            {name}
                        </Typography>
                        <form onSubmit={formik.handleSubmit}>
                            <Stack direction="row" spacing={2}>
                                <Paper
                                    variant="outlined"
                                    sx={{
                                        p: '2px 4px',
                                        display: 'flex',
                                        alignItems: 'center',
                                        minWidth: '33vw',
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
                                        inputProps={{ 'aria-label': 'search' }}
                                    />
                                    <IconButton
                                        type="submit"
                                        sx={{ p: '10px' }}
                                        aria-label="search"
                                    >
                                        <SearchIcon />
                                    </IconButton>
                                </Paper>
                                <FormControl fullWidth sx={{ minWidth: '8vw' }}>
                                    <InputLabel id="searchModelLabel">
                                        Search Model
                                    </InputLabel>
                                    <Select
                                        labelId="searchModelLabel"
                                        id="searchModel"
                                        value={formik.values.model}
                                        onChange={(event: SelectChangeEvent) =>
                                            formik.setFieldValue(
                                                'model',
                                                event.target.value
                                            )
                                        }
                                        label="SearchModel"
                                    >
                                        <MenuItem value="tfidf">
                                            TF-IDF
                                        </MenuItem>
                                        <MenuItem value="bool">Bool</MenuItem>
                                        <MenuItem value="transformers">
                                            Transformers 🚗
                                        </MenuItem>
                                    </Select>
                                </FormControl>
                            </Stack>
                        </form>
                        {searchSuccessful && (
                            <SearchOverview
                                model={model ?? 'TF-IDF'}
                                items={documents}
                            />
                        )}

                        <Divider sx={{ my: 1 }} />
                        <Stack
                            direction="column"
                            justifyContent="center"
                            alignItems="stretch"
                            alignSelf="stretch"
                            spacing={1}
                        >
                            {searchSuccessful
                                ? documents.map((doc, idx) => (
                                      <DocumentSearchResult
                                          key={idx}
                                          documentInfo={doc}
                                          deleteDocument={() => {}}
                                      />
                                  ))
                                : null}
                        </Stack>
                    </Stack>
                </Grid>
                <Grid item xs={0} md={1} lg={2} />
            </Grid>
        </Fragment>
    )
}

export default IndexSearch
