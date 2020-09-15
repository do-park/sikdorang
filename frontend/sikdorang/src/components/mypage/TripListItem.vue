<template>
    <div>
        <div v-for="tripItem in tripList" :key="tripItem.id">
            <h3>{{ tripItem.title }}</h3>
            <p>{{ tripItem.lat }}</p>
            <p>{{ tripItem.lng }}</p>
        </div>
    </div>
</template>

<script>
export default {
    name: "TripListItem",
    props: {
        tripList: Array,
    }
}
</script>

<style>

</style>