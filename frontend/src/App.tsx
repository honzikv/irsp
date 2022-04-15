import React, { Fragment } from 'react'
import './App.css'
import { Container } from '@mui/material'
import { Route, Routes } from 'react-router-dom'

const App = () => {
    return (
        <Fragment>
            <Container>
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/index" element={<Index />} />
                </Routes>
            </Container>
        </Fragment>
    )
}

export default App
