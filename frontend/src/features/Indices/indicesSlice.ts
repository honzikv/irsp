import { createAsyncThunk, createSlice } from '@reduxjs/toolkit'
import axiosInstance from '../../conf/axios'
import { IndexDto } from './indexDtos'

export interface IndicesState {
    indices: IndexDto[] // list of all obtained indices
    loading: boolean // is loading
    err?: string
}

const initialState: IndicesState = { indices: [], loading: true }

const genericErr = 'Error, unable to fetch indices from the API 😟'

// Fetches all indices from the API
export const fetchIndices = createAsyncThunk('indices/fetch', async () => {
    try {
        const { data, status } = await axiosInstance.get('/indices')
        if (status !== 200) {
            return Promise.reject(genericErr)
        }

        if (!data.success) {
            return Promise.reject(data.message)
        }

        // Return the list of indices
        return data.message
    } catch (e: any) {
        return Promise.reject(genericErr)
    }
})

export const indicesSlice = createSlice({
    name: 'indices',
    initialState,
    reducers: {
        // Removes error from the state
        consumeError: (state: IndicesState) => ({
            ...state,
            err: undefined,
        }),
    },

    // Thunks
    extraReducers: (builder) => {
        builder.addCase(fetchIndices.pending, (state) => {
            state.loading = true
        })
        builder.addCase(fetchIndices.fulfilled, (state, action) => {
            return { ...state, loading: false, indices: action.payload }
        })
        builder.addCase(fetchIndices.rejected, (state, action) => {
            return {
                ...state,
                loading: false,
                indices: [],
                err: action.error.message as string,
            }
        })
    },
})

const indicesReducer = indicesSlice.reducer
export default indicesReducer

export const { consumeError } = indicesSlice.actions
