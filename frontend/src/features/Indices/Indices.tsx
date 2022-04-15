import { Button, Container, Divider, Typography } from '@mui/material'
import { Fragment, useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { RootState } from '../../redux/store'
import CreateIndexDialog from './CreateIndexDialog'
import { fetchIndices } from './indicesSlice'

const Indices = () => {

    const dispatch = useDispatch()

    const indices = useSelector((state: RootState) => state.indices.indices)
    

    useEffect(() => {
        dispatch(fetchIndices())
    }, [dispatch])

    return <Container sx={{mx: 1, my: 0}}>

        <Typography sx={{mb: 3}} variant="h3" fontWeight="bold">Indices</Typography>
        <CreateIndexDialog maxWidth='sm' />
        <Divider sx={{my: 2}} />
        
        {JSON.stringify(indices)}
        
        </Container>
}

export default Indices
