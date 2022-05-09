import {
    Container,
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
import { DocumentSearchResultDto } from '../indexDtos'
import SearchOverview from './SearchOverview'
import axiosInstance from '../../../conf/axios'
import { showNotification } from '../../Notification/notificationSlice'
import CreateDocumentDialog from './CreateDocumentDialog'
import { Box } from '@mui/system'

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
                                            ) =>
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
                                alignSelf="stretch"
                                alignItems="flex-end"
                                sx={{ my: 2 }}
                            >
                                <CreateDocumentDialog index={name} />
                            </Stack>
                        )}
                        {searchSuccessful && documents.length > 0 && (
                            <Fragment>
                                <SearchOverview
                                    model={model ?? 'TF-IDF'}
                                    items={documents}
                                />
                                <Divider sx={{ my: 1 }} />
                            </Fragment>
                        )}

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
                    </Fragment>
                </Grid>
                <Grid item xs={0} md={1} lg={2} />
            </Grid>
        </Fragment>
    )
}

export default IndexSearch
