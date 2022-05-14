import { createAsyncThunk, createSlice, current } from '@reduxjs/toolkit'
import axiosInstance from '../../../conf/axios'
import { RootState } from '../../../redux/store'
import { DocumentDto, DocumentSearchResultDto, QueryDto } from '../indexDtos'

/**
 * State for the index search_model
 * This state should be reseted whenever the IndexSearch component is unmounted
 */
export interface IndexSearchState {
    query?: QueryDto
    index?: string
    loading: boolean
    deleteLoading: boolean
    err?: string
    deleteSuccess?: boolean
    // From SearchResultDto
    documents?: DocumentDto[]
    totalDocuments: number
    stopwords?: string[]
}

/**
 * Sends search_model request to the server and updates the state
 */
export const search = createAsyncThunk(
    'indexSearch/search_model',
    async (_, { getState }) => {
        const state = getState() as RootState
        const { query, index } = state.indexSearch // get query and index
        try {
            // Send the request
            const { data } = await axiosInstance.post(
                `/indices/${index}/search`,
                query
            )

            // If we get an error reject with error message
            if (!data.success) {
                return Promise.reject(
                    data.message ??
                        'Unknown error occurred, please try again later'
                )
            }

            // Return the search_model result
            return data.message as DocumentSearchResultDto
        } catch (err: any) {
            return Promise.reject(
                'Error while communicating with the server, please try again later'
            )
        }
    }
)

export const deleteDocument = createAsyncThunk(
    'indexSearch/deleteDocument',
    async (documentDto: DocumentDto, { getState }) => {
        console.log('Deleting document', documentDto)
        const state = getState() as RootState
        const { index } = state.indexSearch
        if (!index) {
            return Promise.reject(
                'Error could not delete document, index is not available 😔'
            )
        }
        try {
            const { data } = await axiosInstance.delete(
                `/indices/${index}/documents/${documentDto.id}`
            )
            if (data.success) {
                return documentDto // return the deleted document dto
            }

            // Else !data.success
            return Promise.reject(
                data.message ?? 'Unknown error occurred, please try again later'
            )
        } catch (err: any) {
            return Promise.reject(
                'Error while communicating with the server, please try again later'
            )
        }
    }
)

const initialState: IndexSearchState = {
    loading: false,
    deleteLoading: false,
    totalDocuments: 0,
}

const IndexSearchStateSlice = createSlice({
    name: 'indexSearch',
    initialState,
    reducers: {
        clear: () => ({} as IndexSearchState), // this is used whenever the user navigates away from the page
        clearSearchResult: (state: IndexSearchState) => ({
            ...state,
            query: undefined,
            searchResult: undefined,
        }), // clears search_model result
        setIndex: (state: IndexSearchState, action: { payload: any }) => ({
            ...state,
            index: action.payload,
        }), // sets the index
        setQuery: (state: IndexSearchState, action: { payload: any }) => ({
            ...state,
            query: action.payload,
        }), // setter for query
        consumeErr: (state: IndexSearchState) => ({ ...state, err: undefined }), // consumes error
        consumeDeleteSuccess: (state: IndexSearchState) => ({
            ...state,
            deleteSuccess: undefined,
        }), // consumes delete success
        setDocument: (state: IndexSearchState, action: any) => {
            const document = action.payload
            if (!state.documents) {
                return { ...state }
            }

            return {
                ...state,
                documents: [...state.documents].map((item) =>
                    item.id === document.id ? document : item
                ),
            }
        },
    },
    extraReducers: (builder) => {
        builder.addCase(search.pending, (state: IndexSearchState) => ({
            ...state,
            loading: true,
        }))
        builder.addCase(search.fulfilled, (state: IndexSearchState, action) => ({
            ...state,
            loading: false,
            ...action.payload,
        }))
        builder.addCase(search.rejected, (state: IndexSearchState, action) => ({
            ...state,
            loading: false,
            err: action.error.message,
        }))

        builder.addCase(deleteDocument.pending, (state: IndexSearchState) => ({
            ...state,
            deleteLoading: true,
        }))
        builder.addCase(deleteDocument.fulfilled, (state: IndexSearchState, action) => {
            if (!state.documents) {
                return {
                    ...state,
                    deleteLoading: false,
                    deleteSuccess: true,
                    totalDocuments: 0,
                }
            }

            // Otherwise remove the deleted item from the search_model result if it exists
            const { documents } = state
            const newDocuments = documents.filter(
                (document) => document.id !== action.payload.id
            )
            return {
                ...state,
                deleteLoading: false,
                deleteSuccess: true,
                documents: newDocuments,
                totalDocuments: state.totalDocuments - 1,
            }
        })
        builder.addCase(deleteDocument.rejected, (state, action) => ({
            ...state,
            deleteLoading: false,
            err: action.error.message,
            deleteSuccess: false,
        }))
    },
})

export const {
    clear,
    setQuery,
    consumeErr,
    clearSearchResult,
    setIndex,
    consumeDeleteSuccess,
    setDocument,
} = IndexSearchStateSlice.actions
const indexSearchReducer = IndexSearchStateSlice.reducer
export default indexSearchReducer
