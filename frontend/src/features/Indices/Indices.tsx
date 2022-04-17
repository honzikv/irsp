import {
    Button,
    Container,
    Divider,
    Grid,
    Stack,
    Typography,
} from '@mui/material'
import { Fragment, useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { RootState } from '../../redux/store'
import CreateIndexDialog from './CreateIndexDialog'
import IndexDetail from './IndexDetail'
import { IndexDto } from './indicesDtos'
import IndicesOverview from './IndicesOverview'
import { fetchIndices } from './indicesSlice'

const Indices = () => {
    const dispatch = useDispatch()

    const indices = useSelector((state: RootState) => state.indices.indices)

    // Some stats mostly used for debugging but looks nice
    const [totalDocuments, setTotalDocuments] = useState(0)
    const [totalIndices, setTotalIndices] = useState(0)

    useEffect(() => {
        dispatch(fetchIndices())
    }, [dispatch])

    // Calculate the stats
    useEffect(() => {
        if (indices) {
            const total = indices.reduce((acc, index) => acc + index.nDocs, 0)
            setTotalDocuments(total)
            setTotalIndices(indices.length)
        }
    }, [indices])

    return (
        <Container sx={{ mx: 1, my: 0 }}>
            <Typography sx={{ mb: 3 }} variant="h3" fontWeight="bold">
                Indices
            </Typography>

            <CreateIndexDialog maxWidth="lg" />
            <Divider sx={{ my: 2 }} />
            {indices.length === 0 ? (
                <Typography align="center" color="text.secondary">
                    No indices were found 😞
                </Typography>
            ) : null}
            <Grid container>
                <Grid item xs={12} md={8}>
                    <Stack direction="column" spacing={2}>
                        {[...indices]
                            .sort((a, b) => a.name.localeCompare(b.name))
                            .map((index, idx) => (
                                <IndexDetail
                                    key={idx}
                                    name={index.name}
                                    nTerms={index.nTerms}
                                    nDocs={index.nDocs}
                                    models={index.models}
                                    exampleDocuments={index.exampleDocuments}
                                />
                            ))}
                    </Stack>
                </Grid>
                <Grid item xs={12} md={4}>
                    {indices.length > 0 ? (
                        <IndicesOverview
                            totalDocuments={totalDocuments}
                            totalIndices={totalIndices}
                        />
                    ) : null}
                </Grid>
            </Grid>
        </Container>
    )
}

export default Indices
