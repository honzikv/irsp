import { Button, Card, CardContent, Stack, Typography } from '@mui/material'
import { FunctionComponent } from 'react'
import { IndexDto } from './indicesDtos'


const IndexDetail: FunctionComponent<IndexDto> = ({ name, nDocs, nTerms, exampleDocuments }) => (
    <Card variant="outlined">
        <CardContent>
            <Typography variant="h5" fontWeight="bold">
                {name}
            </Typography>
            <Typography color="text.secondary">
                {nTerms} terms
            </Typography>
            <Typography color="text.secondary">
                {nDocs} documents
            </Typography>
            <Stack
                direction="row"
                justifyContent="flex-end"
                alignItems="center"
                spacing={1}
            >
                <Button variant="contained" color="secondary">Modify</Button>
                <Button variant="contained">Search</Button>
            </Stack>
        </CardContent>
    </Card>
)

export default IndexDetail
