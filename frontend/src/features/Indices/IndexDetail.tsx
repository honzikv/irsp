import { Divider, IconButton, InputBase, Paper } from '@mui/material'
import { useFormik } from 'formik'
import { Fragment } from 'react'
import { useDispatch } from 'react-redux'
import { useParams } from 'react-router-dom'
import SearchIcon from '@mui/icons-material/Search'

// Detail component which shows the search bar, results and some configuration
const IndexDetail = () => {
    const dispatch = useDispatch()
    const { name } = useParams()

    const initialValues = {
        query: '',
    }

    const formik = useFormik({
        initialValues,
        onSubmit: (values) => {},
    })

    return (
        <Fragment>
            <form onSubmit={formik.handleSubmit}>
                <Paper
                    component="form"
                    sx={{
                        p: '2px 4px',
                        display: 'flex',
                        alignItems: 'center',
                        width: 400,
                    }}
                >
                    <InputBase
                        sx={{ ml: 1, flex: 1 }}
                        placeholder="Search"
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
            </form>
        </Fragment>
    )
}

export default IndexDetail
