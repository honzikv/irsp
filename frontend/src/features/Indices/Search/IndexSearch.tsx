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
import { Fragment } from 'react'
import { useDispatch } from 'react-redux'
import { useParams } from 'react-router-dom'
import SearchIcon from '@mui/icons-material/Search'
import DocumentSearchResult from './DocumentSearchResult'
import { DocumentSearchResultDto } from '../indicesDtos'
import SearchOverview from './SearchOverview'

const sampleDoc: DocumentSearchResultDto = {
    docId: 1,
    text: 'Zombie ipsum reversus ab viral inferno, nam rick grimes malum cerebro. De carne lumbering animata corpora quaeritis. Summus brains sit​​, morbo vel maleficia? De apocalypsi gorger omero undead survivor dictum mauris. Hi mindless mortuis soulless creaturas, imo evil stalking monstra adventus resi dentevil vultus comedat cerebella viventium. Qui animated corpse, cricket bat max brucks terribilem incessu zomby. The voodoo sacerdos flesh eater, suscitat mortuos comedere carnem virus. Zonbi tattered for solum oculi eorum defunctis go lum cerebro. Nescio brains an Undead zombies. Sicut malus putrid voodoo horror. Nigh tofth eliv ingdead.    ',
    score: 0.5,
    additionalProperties: {
        indexName: 'test',
        indexType: 'test',
    },
}

const sampleDoc2: DocumentSearchResultDto = {
    docId: 1,
    text: 'Zombie 🧟 ipsum reversus ab viral inferno, nam rick grimes malum cerebro. De carne lumbering animata corpora quaeritis. Summus brains sit​​, morbo vel maleficia? De apocalypsi gorger omero undead survivor dictum mauris. Hi mindless mortuis soulless creaturas, imo evil stalking monstra adventus resi dentevil vultus comedat cerebella viventium. Qui animated corpse, cricket bat max brucks terribilem incessu zomby. The voodoo sacerdos flesh eater, suscitat mortuos comedere carnem virus. Zonbi tattered for solum oculi eorum defunctis go lum cerebro. Nescio brains an Undead zombies. Sicut malus putrid voodoo horror. Nigh tofth eliv ingdead.    ',
    score: 0.5,
    additionalProperties: {
        indexName: 'test',
        indexType: 'test',
    },
}

const sampleDocs: DocumentSearchResultDto[] = [sampleDoc, sampleDoc2]

// Detail component which shows the search bar, results and some configuration
const IndexSearch = () => {
    const dispatch = useDispatch()
    const { name } = useParams()

    const initialValues = {
        query: '',
        model: 'tfidf',
    }

    const formik = useFormik({
        initialValues,
        onSubmit: (values) => {},
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
                                        onChange={(event: SelectChangeEvent) => formik.setFieldValue('model', event.target.value)}
                                        label="SearchModel"
                                    >
                                        <MenuItem value="tfidf">TF-IDF</MenuItem>
                                        <MenuItem value="bool">Bool</MenuItem>
                                        <MenuItem value="transformers">Transformers 🚗</MenuItem>
                                    </Select>
                                </FormControl>
                            </Stack>
                        </form>

                        <SearchOverview items={sampleDocs} />

                        <Divider sx={{ my: 1 }} />
                        <DocumentSearchResult
                            {...{
                                document: sampleDoc,
                                deleteDocument: () => {},
                            }}
                        />
                    </Stack>
                </Grid>
                <Grid item xs={0} md={1} lg={2} />
            </Grid>
        </Fragment>
    )
}

export default IndexSearch
